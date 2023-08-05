# Author: MetariumProject

# Standard libraries
import time
import os
import io
from pathlib import Path
import json
# Third party libraries
import requests
import multibase
from blake3 import blake3
import ipfshttpclient
from ipfshttpclient import Client
from ipfshttpclient.exceptions import (
    ConnectionError,
    TimeoutError,
    StatusError,
    TimeoutError,
)
from substrateinterface import SubstrateInterface, Keypair
# Metarium libraries
from py_metarium import (
    FUTURE,
)
from py_metarium_listener import (
    QueryParameter,
    TopicListenerStatusListener,
    TopicListenerOperation,
)
from py_metarium_encoder import (
    SubstrateAriKuriAdderAsTopicCommitterNode,
    SubstrateTopicListenerAdderAsConfigurationNode,
    AriKuriAlreadyExistsError,
)
# local libraries
from .exceptions import (
    ServiceDoesNotExistError,
    ServiceInactiveError,
    StorageConnectionRefusedError,
)


class TopicCommitter(object):
    """
        A Yettagam Scribe can perform the following functions:
        [x] Add Arikuris, aka, Kuris to a Topic
        [x] Listen to Topic updates from a Topic Listener
        [#] Connect to a Topic Listener
        [#] Sync with a Topic Listener via IPFS Pub/sub
    """

    SUBSTRATE_EXTRINSIC = "Metarium"

    RECONNECTION_WAIT_DURATION_SECONDS = 5
    MAX_RECONNECTION_ATTEMPTS = 10

    BLAKE3 = "blake3"

    def __init__(self, node_url:str=None, path:str=None, **encoder_kwargs) -> None:
        assert node_url is not None
        assert "mnemonic" in encoder_kwargs or "uri" in encoder_kwargs
        if "mnemonic" in encoder_kwargs:
            self.key_pair = Keypair.create_from_mnemonic(encoder_kwargs["mnemonic"])
        elif "uri" in encoder_kwargs:
            self.key_pair = Keypair.create_from_uri(encoder_kwargs["uri"])

        self.metarium_node_url = node_url

        self.kuri_creator = SubstrateAriKuriAdderAsTopicCommitterNode(url=node_url, **encoder_kwargs)
        self.service_creator = SubstrateTopicListenerAdderAsConfigurationNode(url=node_url, **encoder_kwargs)

        self.file_set = set()
        self.service_set = set()
        self.__setup(node_url=node_url, path=path or f"{Path().resolve()}")
    
    def start(self, topic_id:int=None):
        assert topic_id is not None
        while True:
            time.sleep(2)
            self.auto_upload(topic_id=topic_id)

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
        substrate = SubstrateInterface(url=node_url)
        self.directory = f"{path}/{self.key_pair.ss58_address}/{substrate.chain}"
        self.data_directory = f"{self.directory}/data"
        self.sync_directory = f"{self.directory}/sync"
        # create directories if they don't exist
        self.__set_or_create_directory(self.data_directory)
        self.__set_or_create_directory(self.sync_directory)
        # create mappings.json in data if it doesn't exist
        self.__set_or_create_file(path=f"{self.data_directory}/mappings", extension="json")
    
    def auto_upload(self, topic_id:int=None):
        assert topic_id is not None
        for file in os.listdir(self.data_directory):
            # ignore mappings.json and hidden files
            if file == "mappings.json" or file.startswith("."):
                continue
            if file not in self.file_set:
                self.file_set.add(file)
                kuri_data = {
                    "topic_id": topic_id,
                    "type": "file",
                    "content": os.path.join(self.data_directory, file)
                }
                try:
                    transaction_hash = self.create_kuri(data=kuri_data)
                    if transaction_hash:
                        print(f"New file uploaded: {file}")
                except AriKuriAlreadyExistsError:
                    pass
                self.__update_mappings(data=kuri_data)
    
    def __update_mappings(self, data:dict=None):
        assert data is not None
        with open(f"{self.data_directory}/mappings.json", "r") as f:
            mappings = json.load(f)
        data_hash = self.__blake3_hash(data=data)
        if data_hash not in mappings:
            mappings[data_hash] = data["content"]
            with open(f"{self.data_directory}/mappings.json", "w") as f:
                json.dump(mappings, f)
    
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
        return f"|>blake3|{hasher.hexdigest()}"

    def create_kuri(self, data:dict=None) -> str:
        assert data is not None
        transaction_hash = self.kuri_creator.encode(
            data=data,
            wait_for_inclusion=True,
            wait_for_finalization=False
        )
        
        return transaction_hash
    
    def create_service(self, service_data:dict=None) -> str:
        assert service_data is not None
        transaction_hash = self.service_creator.encode(
            data=service_data,
            wait_for_inclusion=True,
            wait_for_finalization=False
        )
        return transaction_hash
    
    def create_query(self, filters:dict={}) -> list:
        query = []
        for field, value in filters.items():
            query.append(
                QueryParameter(field, f"^{value}$")
            )
        return query

    def __ipfs_pubsub_publish(self, topic:str=None, message:str=None, listener_ip_address:str="127.0.0.1", port:int=5001):
        assert topic is not None
        assert message is not None
        file = io.BytesIO(message if type(message) == bytes else message.encode("utf8"))

        files = {'file': file}

        print(f"Publishing message {message} for topic {topic} to {listener_ip_address}:{port} with files {files} ...")
        requests.post("http://"+listener_ip_address+":"+str(port)+"/api/v0/pubsub/pub?arg="+multibase.encode("base64url",topic).decode("utf8"),files=files)

    def listen_to_topic_updates(self, topic_id:int=None) -> str:
        assert topic_id is not None
        topic_id = str(topic_id)
        # check if topic is un-archived on chain
        query_result = SubstrateInterface(url=self.metarium_node_url).query(
            module=self.__class__.SUBSTRATE_EXTRINSIC,
            storage_function="Topics",
            params=[topic_id],
        )
        topic = query_result.serialize()
        if topic is None:
            raise ServiceDoesNotExistError(f"Topic does not exist: {topic_id}")
        else:
            if topic["archived"]:
                raise ServiceInactiveError(f"Topic has been archived: {topic_id}")
        
        # create directory for topic if it doesn't exist
        topic_directory = f"{self.sync_directory}/{topic_id}"
        self.__set_or_create_directory(f"{topic_directory}")
        listener = TopicListenerStatusListener(self.metarium_node_url)
        filters = {
            "topic_id": f"^{topic_id}$"
        }
        query = self.create_query(filters=filters)
        for block in listener.listen(FUTURE, None, None, query=query):
            
            print(f"block:\n{block}")

            for update in block["extrinsics"]:
                listener = update["caller"]
                # create directory for listener of the topic if it doesn't exist
                listener_directory = f"{self.sync_directory}/{topic_id}/{listener}"
                self.__set_or_create_directory(f"{listener_directory}")
                # create status.txt in listener_directory if it doesn't exist
                self.__set_or_create_file(path=f"{listener_directory}/status", extension="txt")
                # create rff.txt in listener_directory if it doesn't exist
                self.__set_or_create_file(path=f"{listener_directory}/rff", extension="txt")
                # get the status and rff of the listener
                status = update["status"]
                rff = update["rff"]
                with open(f"{listener_directory}/status.txt", "w") as f:
                    f.write(status)
                with open(f"{listener_directory}/rff.txt", "w") as f:
                    f.write(rff)
                print(f"Service status updated: {status}")
                print(f"Service rff updated: {rff}")
                # open rff as IPFS CID
                try:
                    rff_file = self.__ipfs_client.cat(rff)
                    print(f"\n\nRFF FILE CONTENTS:\n{rff_file}\n\n")
                    kuris_to_pubish = [decoded for decoded in rff_file.decode("utf-8").split("\n") if decoded != ""]
                    print(f"KURIS TO PUBLISH:\n{kuris_to_pubish}\n")
                    with open(f"{self.data_directory}/mappings.json", "r") as f:
                        mappings = json.load(f)
                        for kuri in kuris_to_pubish:
                            # check if kuri exists in mappings.json
                            if kuri in mappings:
                                content = mappings[kuri]
                                print(f"\nKURI FOUND IN MAPPINGS : {content}")
                                # get file name from the content
                                file_name = content.split("/")[-1]
                                # create IPFS CID from content
                                ipfs_cid = self.__ipfs_client.add(content)
                                print(f"IPFS CID CREATED : {ipfs_cid['Hash']}")
                                # publish IPFS CID to IPFS pubsub
                                try:
                                    message = {"cid": ipfs_cid['Hash'], "file_name": file_name}
                                    self.__ipfs_pubsub_publish(topic=kuri, message=json.dumps(message))
                                except Exception as error:
                                    print(f"IPFS pubsub publish error: {error}")
                except TimeoutError:
                    print(f"IPFS timeout error. Is your IPFS client connected to the Service's IPFS client?\n{TimeoutError}")
                    continue

