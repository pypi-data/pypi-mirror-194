import asyncio

import json

from substrateinterface.exceptions import SubstrateRequestException

from py_metarium_listener import (
    QueryParameter,
    AriKuriListener,
    ArikuriOperation,
)
from .exceptions import (
    StorageError,
)

OPERATION = ArikuriOperation()

class KuriSyncBase(object):

    def __init__(self, metarium_node_url:str=None) -> None:
        assert metarium_node_url is not None
        self.metarium_node_url = metarium_node_url

        self.CACHE_KEY_CURRENT_BLOCK_NUMBER = "current_block_number"

        self.__reset_cache()

    def __reset_cache(self) -> None:
        self.__cache = {}
    
    def __cached(self, key, default:any=None) -> None:
            return self.__cache.get(f"{key}", default)

    def __update_cache(self, key, value) -> None:
        self.__cache.update({f"{key}": value})

    def get_sync_location(self, filters:dict={}) -> str:
        raise NotImplementedError

    def save_kuri(self, kuri, filters:dict={}):
        raise NotImplementedError
    
    def delete_kuri(self, kuri, filters:dict={}):
        raise NotImplementedError

    def __synced(self, filters:dict={}):
        sync_location = self.get_sync_location(filters=filters)
        try:
            with open(f"{sync_location}", "r") as readable:
                synced = json.load(readable)
        except FileNotFoundError:
            synced = {}
        
        return synced, sync_location

    def __synced_chain_block_number(self, filters:dict={}) -> int:
        synced, sync_location = self.__synced(filters=filters)
        return int(synced.get("chain", 0))

    def __synced_kuri_block_number(self, kuri:str, filters:dict={}) -> int:
        synced, sync_location = self.__synced(filters=filters)
        return int(synced.get(kuri, 0))

    def __sync_chain_block_number(self, filters:dict={}):
        synced, sync_location = self.__synced(filters=filters)
        block_number = self.__cached(self.CACHE_KEY_CURRENT_BLOCK_NUMBER, default=0)
        print(f"{sync_location} : syncing chain at block number {block_number} ...")
        to_sync = {
            f"chain": f"{block_number}"
        }
        print(f"pre-sync : {synced}")
        print(f"to sync : {to_sync}")
        synced.update(to_sync)
        with open(f"{sync_location}", "w") as writable:
            json.dump(synced, writable)
        print(f"post-sync : {synced}")

    def __sync_kuri_block_number(self, kuri:str, filters:dict={}):
        synced, sync_location = self.__synced(filters=filters)
        block_number = self.__cached(self.CACHE_KEY_CURRENT_BLOCK_NUMBER, default=0)
        print(f"{sync_location} : syncing kuri {kuri} at block number {block_number} ...")
        to_sync = {
            f"{kuri}": f"{block_number}"
        }
        print(f"pre-sync : {synced}")
        print(f"to sync : {to_sync}")
        synced.update(to_sync)
        with open(f"{sync_location}", "w") as writable:
            json.dump(synced, writable)
        print(f"post-sync : {synced}")

    def create_query(self, filters:dict={}) -> list:
        query = []
        for field, value in filters.items():
            query.append(
                QueryParameter(field, f"^{value}$")
            )
        return query

    def __sync(self, 
                direction:str, start_block_hash:str, block_count:int, query:list,
                listener:AriKuriListener, tip_block_number:int, filters:dict={},
                sync_until_tip:bool=False
            ):
        print(f"start syncing from {start_block_hash} ...")
        for block in listener.listen(direction, start_block_hash, block_count, query=query):
            print(f"block:\n{block}")
            if sync_until_tip and block["block_number"] >= tip_block_number:
                print(f"\n\n\nkuris synced until last recorded finalized block number {tip_block_number}\n\n")
                break

            print(f"block:\n{block}")

            self.__update_cache(self.CACHE_KEY_CURRENT_BLOCK_NUMBER, block["block_number"])
            self.__sync_chain_block_number(filters=filters)

            for kuri_info in block["extrinsics"]:
                kuri = kuri_info["kuri"]
                if self.__synced_kuri_block_number(kuri=kuri, filters=filters) <= self.__cached(self.CACHE_KEY_CURRENT_BLOCK_NUMBER, default=0):
                    # sync kuri
                    self.__sync_kuri_block_number(kuri=kuri, filters=filters)
                    try:
                        if kuri_info["call_function"] in (
                                OPERATION.add, OPERATION.accept_multiple
                            ):
                            # save kuri by pinning it's CID
                            self.save_kuri(kuri=kuri, filters=filters)
                        elif kuri_info["call_function"] in (
                                OPERATION.delete, OPERATION.transfer_multiple
                            ):
                            # delete kuri by un-pinning it's CID
                            self.delete_kuri(kuri=kuri, filters=filters)
                    except StorageError as err:
                        print(f"storage error : {err}")

    def sync(self,
            direction:str, start_block_number:any=None, block_count:any=None, finalized_only:bool=False,
            filters:dict={}
        ):
        # reset cache
        self.__reset_cache()
        # set up listener
        listener = AriKuriListener(self.metarium_node_url)
        # print(f"{listener.info()}")
        # sanitize inputs
        ## verify start_block_number
        ### get synced chain block number
        synced_chain_block_number = self.__synced_chain_block_number(filters=filters)
        ## set start_block_number
        if start_block_number and start_block_number > synced_chain_block_number:
            print(f"start_block_number {start_block_number} is later than synced_chain_block_number {synced_chain_block_number}")
            print(f"resetting start_block_number to {synced_chain_block_number}")
        start_block_number = synced_chain_block_number
        ### get tip block number
        tip_block_number = listener.decoder().get_tip_number(finalized_only=finalized_only)
        if synced_chain_block_number > tip_block_number:
            print(f"synced_chain_block_number {synced_chain_block_number} is later than tip_block_number {tip_block_number}")
            print(f"resetting start_block_number to {tip_block_number}")
            start_block_number = tip_block_number
        filters = filters or {}
        ## set up listener parameters
        ### start_block_hash
        start_block_hash = listener.decoder().get_block_hash_from_block_number(start_block_number)
        ### query
        query = self.create_query(filters=filters)
        # set up storage info
        storage_info = {}
        # update cache
        self.__update_cache(self.CACHE_KEY_CURRENT_BLOCK_NUMBER, start_block_number)
        # log:DEBUG
        print(f"tip_block_number : {tip_block_number}")
        print(f"synced_chain_block_number : {synced_chain_block_number}")
        print(f"start_block_hash : {start_block_hash}")
        print(f"query : {query}")
        print(f"storage_info : {storage_info}")

        try:
            self.__sync(
                direction=direction, start_block_hash=start_block_hash, block_count=block_count, query=query,
                listener=listener, tip_block_number=tip_block_number, filters=filters
            )
        except SubstrateRequestException as err:
            if str(err) == "{'code': -32000, 'message': 'Client error: UnknownBlock: State already discarded for "+start_block_hash+"'}":
                print(f"State already discarded for {start_block_hash}")
                print(f"resetting start_block_number to {tip_block_number - 200}")
                start_block_number = tip_block_number - 200
                start_block_hash = listener.decoder().get_block_hash_from_block_number(start_block_number)
                print(f"start_block_hash : {start_block_hash}")
                self.__sync(
                    direction=direction, start_block_hash=start_block_hash, block_count=block_count, query=query,
                    listener=listener, tip_block_number=tip_block_number, filters=filters
                )
        


