# Author: MetariumProject

# Standard libraries
import time
import os
import threading
from pathlib import Path
import json
import asyncio
# Third party libraries
import requests
import multibase
import ipfshttpclient
from ipfshttpclient import Client
from ipfshttpclient.exceptions import (
    ConnectionError,
    TimeoutError,
)
from blake3 import blake3
from substrateinterface import SubstrateInterface, Keypair
# Metarium libraries
from py_metarium import (
    FUTURE,
)
from py_metarium_encoder import (
    SubstrateStatusUpdaterAsTopicListenerNode,
)
# local libraries
from .exceptions import (
    StorageConnectionRefusedError,
    StorageError,
)
from .storage import (
    KuriSyncBase,
)


class TopicListener(KuriSyncBase):

    RECONNECTION_WAIT_DURATION_SECONDS = 5
    MAX_RECONNECTION_ATTEMPTS = 10

    BLAKE3 = "blake3"

    """
        A Yettagam TopicListener can perform the following functions:
        [x] Publish it's own status
        [x] Listen to a Topic's kuris
        [#] Sync with a Topic Committer via IPFS Pub/sub
    """

    def __init__(self, node_url:str=None, path:str=None, **encoder_kwargs) -> None:
        assert node_url is not None
        assert "mnemonic" in encoder_kwargs or "uri" in encoder_kwargs
        super().__init__(node_url)
        if "mnemonic" in encoder_kwargs:
            self.key_pair = Keypair.create_from_mnemonic(encoder_kwargs["mnemonic"])
        elif "uri" in encoder_kwargs:
            self.key_pair = Keypair.create_from_uri(encoder_kwargs["uri"])
        
        self.__setup(node_url=node_url, path=path or f"{Path().resolve()}")

        self.listener_updater = SubstrateStatusUpdaterAsTopicListenerNode(url=node_url, **encoder_kwargs)

        self.__subscribers = {}

    def __set_or_create_directory(self, path:str):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def __set_or_create_file(self, path:str=None, extension:str=None):
        assert path is not None
        assert extension is not None
        if not os.path.exists(f"{path}.{extension}"):
            with open(f"{path}.{extension}", "w") as f:
                if extension == "json":
                    f.write("{}")
                elif extension == "txt":
                    f.write("")

    def __setup_ipfs_client(self):
        reconnection_attempts = 1
        while True:
            try:
                self.__ipfs_client = ipfshttpclient.connect(session=True)
            except ConnectionError:
                if reconnection_attempts == self.__class__.MAX_RECONNECTION_ATTEMPTS:
                    print(f"IPFS connection terminated after {reconnection_attempts} attempts.")
                    raise StorageConnectionRefusedError
                print(f"IPFS connection refused. Retrying in {self.__class__.RECONNECTION_WAIT_DURATION_SECONDS} seconds ...")
                reconnection_attempts += 1
                time.sleep(self.__class__.RECONNECTION_WAIT_DURATION_SECONDS)
                continue
            break

    def __setup(self, node_url:str=None, path:str=None):
        assert node_url is not None
        assert path is not None
        # IPFS
        self.__setup_ipfs_client()
        # directories
        self.topic_set = set()
        substrate = SubstrateInterface(url=node_url)
        self.directory = f"{path}/{self.key_pair.ss58_address}/{substrate.chain}"
        self.data_directory = f"{self.directory}/data"
        self.sync_directory = f"{self.directory}/sync"
        # create directories if they don't exist
        self.__set_or_create_directory(self.data_directory)
        self.__set_or_create_directory(self.sync_directory)
        # create mappings.json in data if it doesn't exist
        self.__set_or_create_file(path=f"{self.data_directory}/mappings", extension="json")
        # create status.txt in sync if it doesn't exist
        self.__set_or_create_file(path=f"{self.sync_directory}/status", extension="txt")
        # create rff.txt in sync if it doesn't exist
        self.__set_or_create_file(path=f"{self.sync_directory}/rff", extension="txt")
    
    def __blake3_hash(self, data:dict=None) -> str:
        # Create a Blake3 hash object
        hasher = blake3(max_threads=blake3.AUTO)
        with open(data["content"], "rb") as f:
            counter = 0
            while True:
                counter += 1
                content = f.read(1024)
                if not content:
                    break
                hasher.update(content)
        return f"|>{self.__class__.BLAKE3}|{hasher.hexdigest()}"

    async def publish_status(self, topic_id:int=None) -> str:
        assert topic_id is not None
        listener_data = {
            "topic_id": topic_id,
            "status": f"{self.sync_directory}/status.txt",
            "rff": self.__ipfs_client.add(f"{self.sync_directory}/rff.txt")["Hash"],
        }

        transaction_hash = self.listener_updater.encode(
            data=listener_data,
            wait_for_inclusion=True,
            wait_for_finalization=False
        )
        yield transaction_hash
    
    async def periodic_publish_status(self, topic_id:int=None, interval:int=10):
        assert topic_id is not None
        while True:
            async for transaction_hash in self.publish_status(topic_id=topic_id):
                print(f"Published status with transaction hash: {transaction_hash}")
            await asyncio.sleep(interval)

    def kuri_registry_file_name(self, topic_id:str=None) -> str:
        assert topic_id is not None
        return f"{self.sync_directory}/{topic_id}/kuris.json"

    def get_sync_location(self, filters:dict={}) -> str:
        return self.kuri_registry_file_name(topic_id=filters["topic_id"][1:-1])

    def __handle_subscription(self, data, seqno, topic_ids, cid, subscription):
        print(f"\n\nSUBSCRIBED MESSAGE RECIEVED!")
        print(f"Data: {data}")
        print(f"Seqno: {seqno}")
        print(f"Topic IDs: {topic_ids}")
        print(f"Message CID: {cid}")
        print(f"\n\n")
        kuri = topic_ids[0].decode("utf-8")
        data = json.loads(data.decode("utf-8"))
        kuri_cid = data["cid"]
        kuri_file_name = data["file_name"]
        # check if kuri exists in data/mappings.json
        with open(f"{self.data_directory}/mappings.json", "r") as f:
            mappings = json.load(f)
            if kuri not in mappings:
                print(f"\nKURI NOT FOUND IN MAPPINGS : {kuri}")
                try:
                    # pin the file
                    print(f"Pinning file CID ({kuri_cid}) for kuri {kuri} ...")
                    res = self.__ipfs_client.pin.add(kuri_cid)
                    print(f"pin response : {res}")
                except TimeoutError:
                    raise StorageError(
                        f"\n\n\n\nEncountered an error while saving kuri {kuri}\n\nIs the CID {kuri_cid} visible on your IPFS client?\n\n"
                    )
                # add the file from cid to data directory
                print(f"Adding file CID ({kuri_cid}) for kuri {kuri} to data directory ...")
                with open(f"{self.data_directory}/{kuri_file_name}", "wb") as f:
                    f.write(self.__ipfs_client.cat(kuri_cid))
                # add the kuri to mappings
                mappings[kuri] = f"{self.data_directory}/{kuri_file_name}"
                with open(f"{self.data_directory}/mappings.json", "w") as f:
                    json.dump(mappings, f)
                print(f"KURI {kuri} added to mappings")
                # remove the kuri from sync/rff.txt if it exists
                kuris_in_rff = []
                with open(f"{self.sync_directory}/rff.txt", "r") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            kuris_in_rff.append(line)
                print(f"{kuris_in_rff = }")
                if kuri in kuris_in_rff:
                    kuris_in_rff.remove(kuri)
                    with open(f"{self.sync_directory}/rff.txt", "w") as f:
                        for kuri in kuris_in_rff:
                            f.write(f"{kuri}")
                # unsubscribe from the kuri
                self.__ipfs_pubsub_unsubscribe(topic=kuri)

    def __ipfs_pubsub_unsubscribe(self, topic:str=None):
        assert topic is not None
        self.__unsubscribe(topic=topic)

    def __ipfs_pubsub_subscribe(self, topic:str=None, listener_ip_address:str="127.0.0.1"):
        assert topic is not None
        if not topic in self.__subscribers.keys():
            self.__subscribers[topic] = [[],True]
        self.__subscribers[topic][1] = True

        th = threading.Thread(target=self.__subscribe, kwargs={"topic":topic})
        th.daemon = True
        th.start()
        
    def __subscribe(self, topic:str=None, ip:str="127.0.0.1", port:int=5001):
        seq_offset = -1
        with requests.post("http://"+ip+":"+str(port)+"/api/v0/pubsub/sub?arg="+multibase.encode("base64url", topic).decode("utf8"), stream=True) as r:
            self.__subscribers[topic][0].append(r)
            while True:
                try:
                    for m in r.iter_lines():
                        j = json.loads(m.decode("utf8"))
                        j["data"] = multibase.decode(j["data"])
                        j["seqno"] = int.from_bytes(multibase.decode(j["seqno"]),"big")

                        if seq_offset == -1:
                            seq_offset = j["seqno"]
                        j["seqno"] = j["seqno"] - seq_offset

                        for i in range(len(j["topicIDs"])):
                            j["topicIDs"][i] = multibase.decode(j["topicIDs"][i])

                        self.__handle_subscription(data=j["data"],seqno=j["seqno"],topic_ids=j["topicIDs"],cid=j["from"], subscription=r)
                except:
                    if not topic in self.__subscribers.keys() or self.__subscribers[topic][1] == False:
                        return

    def __unsubscribe(self, topic:str=None):
        if topic in self.__subscribers.keys():
            print(f"Unsubscribing from topic: {topic}")
            for i in range(len(self.__subscribers[topic][0])-1,-1,-1):
                if not self.__subscribers[topic][0][i] is None:
                    self.__subscribers[topic][0][i].close()
                    self.__subscribers[topic][0][i] = None
            self.__subscribers[topic][1] = False
        else:
            print(f"Topic {topic} not found in subscribers!")

    def save_kuri(self, kuri, filters:dict={}):
        # save kuri to status.txt if it doesn't exist
        kuris_in_status = []
        with open(f"{self.sync_directory}/status.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    kuris_in_status.append(line)
        print(f"{kuris_in_status = }")
        if kuri not in kuris_in_status:
            kuris_in_status.append(kuri)
            with open(f"{self.sync_directory}/status.txt", "a") as f:
                f.write(f"\n{kuri}")
        # check if kuri exists in data/mappings.json
        with open(f"{self.data_directory}/mappings.json", "r") as f:
            mappings = json.load(f)
            if kuri not in mappings:
                print(f"\nKURI NOT FOUND IN MAPPINGS : {kuri}")
                # if not, add it to sync/rff.txt if it doesn't exist
                kuris_in_rff = []
                with open(f"{self.sync_directory}/rff.txt", "r") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            kuris_in_rff.append(line)
                print(f"{kuris_in_rff = }")
                if kuri not in kuris_in_rff:
                    with open(f"{self.sync_directory}/rff.txt", "a") as f:
                        f.write(f"\n{kuri}")
                print(f"SUBSCRIBING TO KURI: {kuri}")
                # subscribe to kuri in via pubsub
                try:
                    self.__ipfs_pubsub_subscribe(topic=kuri)
                except Exception as error:
                    print(f"Error subscribing to {kuri}: {error}")

    def sync_with_topic(self,
            topic_id:int=None,
            direction:str=None, start_block_number:any=None, block_count:any=None, finalized_only:bool=False
        ) -> None:
        assert topic_id is not None
        topic_id = str(topic_id)
        direction = direction or FUTURE
        # kuri_prefix = kuri_prefix or self.__class__.BLAKE3
        self.topic_set.add(topic_id)
        # create sync/topic_id if it doesn't exist
        self.__set_or_create_directory(f"{self.sync_directory}/{topic_id}")
        # create kuris.json in sync/topic_id if it doesn't exist
        self.__set_or_create_file(path=f"{self.sync_directory}/{topic_id}/kuris", extension="json")
        # filters = {
        #     "kuri": f"^\|\>{kuri_prefix}\|.*",
        #     "caller": f"^{scribe}$"
        # }
        filters = {
            "topic_id": f"^{topic_id}$"
        }
        self.sync(direction, start_block_number, block_count, finalized_only, filters=filters)
