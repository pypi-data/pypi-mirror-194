#!/usr/bin/env python3
from ordered_set import OrderedSet

from eigenapi_client.endpoints.LatestBlockApi import LatestBlockApi
from eigenapi_client.endpoints.PoolSandwichedApi import PoolSandwichedApi
from eigenapi_client.endpoints.TransactionApi import TransactionApi
from eigenapi_client.endpoints.StatusApi import StatusApi
from eigenapi_client.endpoints.schema import LatestBlock, Transaction, ERROR_CODE

import asyncio
import json
import ssl
import certifi
import websockets
from websockets.exceptions import InvalidStatusCode


class Client(object):
    def __init__(self, apikey: str, host: str = 'api.eigenapi.io'):
        self.apikey = apikey
        self.host = host
        self._local_subscription_cache = OrderedSetQueue(maxsize=1000)

    def status(self):
        return StatusApi().do_request()

    def block_latest(self, chain: str) -> LatestBlock:
        return LatestBlockApi(self.apikey).do_request(chain=chain)

    def transactions(self, chain: str, filter_type: str = None, start: int = None, end: int = None, limit: int = 100):
        return TransactionApi(self.apikey)\
            .do_request(chain=chain, filter_type=filter_type, start=start, end=end, limit=limit)

    def pool_sandwiched(self, chain: str, duration: int = 30, page: int = 0, limit: int = 100):
        return PoolSandwichedApi(self.apikey).do_request(chain=chain, duration=duration, page=page, limit=limit)

    def subscribe_transactions(self, chain: str = 'all', filter_type: str = 'all',
                               filter_duplicate: bool = True, callback=None):

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.__execute_sub__(chain, filter_type, filter_duplicate, callback))
        finally:
            loop.close()

    def __auto_remove_duplicate_transactions__(self, transaction: Transaction) -> Transaction:
        if not self._local_subscription_cache.__contains__(transaction):
            self._local_subscription_cache.put(transaction)
            return transaction
        else:
            print('duplicated transaction received:', transaction['transactionHash'])
            return None

    async def __execute_sub__(self, chain: str = 'all', filter_type: str = 'all',
                              filter_duplicate: bool = True, callback=None):

        url = f"wss://{self.host}/ws?chain={chain}&type={filter_type}&apikey={self.apikey}"
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(certifi.where())
        try:
            async with websockets.connect(url, ssl=ssl_context) as ws:
                while True:
                    recv_text = await ws.recv()
                    data_dict = json.loads(recv_text)
                    if callback is not None:
                        transaction = Transaction(data_dict)
                        if filter_duplicate:
                            transaction = self.__auto_remove_duplicate_transactions__(transaction)
                            if transaction is not None:
                                callback(transaction)
        except InvalidStatusCode as e:
            if e.status_code in ERROR_CODE:
                raise Exception(e.status_code, ERROR_CODE[e.status_code])
            else:
                raise Exception(e.status_code, str(e))
        except Exception as e:
            raise Exception(str(e))


class OrderedSetQueue(object):
    def __init__(self, maxsize: int = 1000):
        self._max_size = maxsize
        self.data = []

    def put(self, item):
        if len(self.data) > self._max_size:
            self.data.sort(key=lambda element: element.get_id)
            self.data.pop(0)
        self.data.append(item)

    def __contains__(self, item):
        return self.data.__contains__(item)
