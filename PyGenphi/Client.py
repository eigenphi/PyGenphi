import datetime
import json
import uuid
from datetime import timedelta
import asyncio
import aiohttp
from urllib.parse import urlunsplit, urlencode
from decimal import *
import os

from PyGenphi.enum import *


class Client(object):

    def __init__(self):
        pass

    def __init__(self,
                 scheme: str = "http",
                 host: str = "127.0.0.1",
                 port: int = 80,
                 api_key: str = None):
        self.scheme = scheme
        self.host = host
        self.port = port
        self.api_key = api_key

    def make_url(self, locator, symbol, category, date):
        # http://127.0.0.1/kline/binance_main/ETHUSDT-2017-12-23.jsonl
        # http://127.0.0.1/crosschain/anyswap/ALL-ALL.jsonl

        url = category.value + '/' + locator.value + '/' + symbol.upper() + '-' + date + '.jsonl'
        return url

    async def job(self, session, url):
        # 声明为异步函数
        name = url.replace('%23', '-')
        full_name = os.path.join('.data', name)

        url = self.scheme + '://' + self.host + ':' + str(self.port) + '/' + url

        # 获得名字
        f = await session.get(url)
        # 触发到await就切换，等待get到数据
        content = await f.read()
        # 读取内容
        with open(str(full_name), "wb") as fout:
            # 写入文件
            fout.write(content)
        return str(url)

    async def download(self, loop, url):
        async with aiohttp.ClientSession() as session:
            # 建立会话 session
            tasks = [loop.create_task(self.job(session, url[_])) for _ in range(len(url))]
            # 建立所有任务
            finshed, unfinshed = await asyncio.wait(tasks)
            # 触发await，等待任务完成
            all_results = [r.result() for r in finshed]
            # 获取所有结果
            # print("ALL RESULTS:" + str(all_results))

    @staticmethod
    def __mkdir__(path):
        path = path.strip()
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        else:
            return False

    def merge_file(self, url_list, req_id) -> list:

        content = []
        full_name = os.path.join('.data/', req_id + '.jsonl')
        with open(full_name, 'w') as outfile:
            for fname in url_list:
                fname = fname.replace('%23', '-')
                with open(os.path.join('.data/', fname)) as infile:
                    for line in infile:
                        content.append(line)
                        outfile.write(line)

        return content

    def __get_from_multi_files__(self, req_id: str, locator, category, symbol: str, start: str, end: str) -> list:
        delta_1d = timedelta(days=1)
        start_datetime = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_datetime = datetime.datetime.strptime(end, "%Y-%m-%d")
        delta = end_datetime - start_datetime
        start = start_datetime
        i = 1

        url_list = [self.make_url(locator, symbol, category, start.strftime("%Y-%m-%d"))]
        while i <= delta.days:
            start = start + delta_1d
            url_list.append(self.make_url(locator, symbol, category, start.strftime("%Y-%m-%d")))
            i += 1

        loop = asyncio.get_event_loop()

        loop.run_until_complete(self.download(loop, url_list))
        return self.merge_file(url_list, req_id)

    def __get_from_one_file__(self, req_id: str, locator, category, symbol='ALL') -> list:
        url = self.make_url(locator, symbol, category, 'ALL')

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.download(loop, [url]))
        return self.merge_file(url, req_id)

    def get(self, locator, category, symbol='ALL', start='ALL', end='ALL', request_id=str(uuid.uuid4())) -> list:

        Client.__mkdir__('.data')
        Client.__mkdir__(os.path.join('.data', category.value))
        Client.__mkdir__(os.path.join('.data', category.value, locator.value))
        print("Downloading data files, please wait....")
        if start == 'ALL' or end == 'ALL':
            data = self.__get_from_one_file__(request_id, locator, category, symbol)
        else:
            data = self.__get_from_multi_files__(request_id, locator, category, symbol, start, end)
        return [json.loads(item) for item in data]

    async def __request(self, url,
                        method: str = "get",
                        data: str = None) -> str:
        async with aiohttp.ClientSession() as session:
            headers = {}
            if self.api_key is not None:
                headers["APIKey"] = self.api_key
            if method == "get":
                async with session.get(url, headers=headers) as resp:
                    return await resp.json()
            elif method == "post":
                headers["Content-Type"] = "application/json"
                async with session.post(url, data=data, headers=headers) as resp:
                    print(resp)
                    return await resp.json()

    def __fix_transaction_value_type(self, transaction: dict) -> dict:
        for field in ['transactionValue']:
            if transaction.get(field):
                transaction[field] = Decimal(transaction[field])
        return transaction

    def __fix_data_parsed_value_type(self, data_parsed: dict) -> dict:
        for field in ['tokenAmount', 'reserve0', 'reserve1', 'amount0In', 'amount1In', 'amount0Out', 'amount1Out']:
            if data_parsed.get(field):
                data_parsed[field] = Decimal(data_parsed[field])
        return data_parsed

    def __fix_event_log_data(self, d: dict) -> dict:
        if d.get('dataParsed'):
            d['dataParsed'] = self.__fix_data_parsed_value_type(d['dataParsed'])
        return d

    def __fix_transaction_data(self, d: dict) -> dict:
        d = self.__fix_transaction_value_type(d)
        if d.get('logs'):
            d['logs'] = list(map(lambda log: self.__fix_event_log_data(log),
                                 d['logs']))
        return d

    def __fix_get_transaction_by_hash_response(self, response: dict) -> dict:
        if response.get('result'):
            response['result'] = self.__fix_transaction_data(response['result'])
        return response

    def get_transaction_by_hash(self,
                                tx_hash: str,
                                client_id="_",
                                locator: Locator = Locator.BSC) -> dict:
        path = "/v1/dataservice/transaction_by_hash/"
        query = urlencode(dict(id=client_id, locator=locator.value, tx_hash=tx_hash))
        url = urlunsplit((self.scheme, self.host + ":" + str(self.port), path, query, ""))
        print(f"url: {url}")
        return self.__fix_get_transaction_by_hash_response(asyncio.run(self.__request(url)))

    def __fix_get_transactions_by_address_response(self, response: dict) -> dict:
        if response.get('result'):
            response['result'] = list(map(lambda transaction: self.__fix_transaction_data(transaction),
                                          response['result']))
        return response

    def get_transactions_by_address(self,
                                    address: str,
                                    client_id: str = "_",
                                    locator: Locator = Locator.BSC,
                                    mode: AddressMode = AddressMode.ALL,
                                    columns: list = [],  # TODO NOT support yet
                                    first: bool = False,
                                    last: bool = False,
                                    block_number_start=None,
                                    block_number_end=None,
                                    block_timestamp_start=None,
                                    block_timestamp_end=None) -> dict:
        path = "/v1/dataservice/transactions_by_address/"
        query_params = dict(id=client_id,
                            locator=locator.value,
                            address=address,
                            mode=mode.value,
                            columns=columns,
                            first=("true" if first else "false"),
                            last=("true" if last else "false"))
        if block_number_start:
            query_params['blockNumberStart'] = block_number_start
        if block_number_end:
            query_params['blockNumberEnd'] = block_number_end
        if block_timestamp_start:
            query_params['blockTimestampStart'] = block_timestamp_start
        if block_timestamp_end:
            query_params['blockTimestampEnd'] = block_timestamp_end
        query = urlencode(query_params)
        url = urlunsplit((self.scheme, self.host + ":" + str(self.port), path, query, ""))
        return self.__fix_get_transactions_by_address_response(asyncio.run(self.__request(url)))

    def __fix_get_token_transfers_by_address_response(self, response: dict) -> dict:
        if response.get('result'):
            response['result'] = list(map(lambda transaction: self.__fix_event_log_data(transaction),
                                          response['result']))
        return response

    def get_token_transfers_by_address(self,
                                       address: str,
                                       client_id: str = "_",
                                       locator: Locator = Locator.BSC,
                                       mode: AddressMode = AddressMode.ALL,
                                       columns: list = [],  # TODO NOT support yet
                                       first: bool = False,
                                       last: bool = False,
                                       block_number_start=None,
                                       block_number_end=None,
                                       block_timestamp_start=None,
                                       block_timestamp_end=None) -> dict:
        path = "/v1/dataservice/token_transfers_by_address/"
        query_params = dict(id=client_id,
                            locator=locator.value,
                            address=address,
                            mode=mode.value,
                            columns=columns,
                            first=("true" if first else "false"),
                            last=("true" if last else "false"))
        if block_number_start:
            query_params['blockNumberStart'] = block_number_start
        if block_number_end:
            query_params['blockNumberEnd'] = block_number_end
        if block_timestamp_start:
            query_params['blockTimestampStart'] = block_timestamp_start
        if block_timestamp_end:
            query_params['blockTimestampEnd'] = block_timestamp_end
        query = urlencode(query_params)
        url = urlunsplit((self.scheme, self.host + ":" + str(self.port), path, query, ""))
        response = asyncio.run(self.__request(url))
        return self.__fix_get_token_transfers_by_address_response(response)

    def get_transactions_by_block_number(self,
                                         block_number: int,
                                         client_id: str = "_",
                                         locator: Locator = Locator.BSC) -> dict:

        path = "/v1/dataservice/transactions_by_block_number/"
        query_params = dict(block_number=block_number,
                            id=client_id,
                            locator=locator.value)
        query = urlencode(query_params)
        url = urlunsplit((self.scheme, self.host + ":" + str(self.port), path, query, ""))
        response = asyncio.run(self.__request(url))
        return self.__fix_get_transactions_by_address_response(response)

    def __fix_get_tick_response(self, response: dict) -> dict:
        if response.get('result'):
            response['result'] = list(map(lambda transaction: self.__fix_data_parsed_value_type(transaction),
                                          response['result']))
        return response

    def get_tick(self,
                 lp_addrs: list = None,
                 block_number_start: int = None,
                 block_number_end: int = None,
                 block_timestamp_start: int = None,
                 block_timestamp_end: int = None,
                 client_id: str = "_",
                 locator: Locator = Locator.BSC,
                 page: int = 0,
                 page_size: int = 100):
        path = "/v1/dataservice/tick/"
        query_params = dict(id=client_id,
                            chain=locator.value,
                            pageNum=page,
                            pageSize=page_size)
        if lp_addrs:
            query_params['lpAddrs'] = lp_addrs
        if block_number_start is not None:
            query_params['blockStart'] = block_number_start
        if block_number_end is not None:
            query_params['blockEnd'] = block_number_end
        if block_timestamp_start is not None:
            query_params['startTime'] = block_timestamp_start
        if block_timestamp_end is not None:
            query_params['endTime'] = block_timestamp_end
        query = ""
        data = json.dumps(query_params)
        url = urlunsplit((self.scheme, self.host + ":" + str(self.port), path, query, ""))
        response = asyncio.run(self.__request(url, method="post", data=data))
        return self.__fix_get_tick_response(response)

    def get_tag_lp(self,
                   lp_address: str = None,
                   is_secure: bool = None,
                   locator: Locator = Locator.BSC,
                   client_id: str = "_",
                   page: int = 0,
                   page_size: int = 100) -> dict:
        path = "/v1/dataservice/tag/lp/"
        query_params = dict(id=client_id,
                            chain=locator.value,
                            pageNum=page,
                            pageSize=page_size)
        if lp_address:
            query_params['LPAddress'] = lp_address
        if is_secure is not None:
            query_params['isSecure'] = "true" if is_secure else "false"
        query = urlencode(query_params)
        url = urlunsplit((self.scheme, self.host + ":" + str(self.port), path, query, ""))
        response = asyncio.run(self.__request(url))
        return response

    def get_tag_lp_pairs(self,
                         org_id: str = None,
                         arbitrage_type: ArbitrageType = None,
                         start_time: int = None,
                         end_time: int = None,
                         locator: Locator = Locator.BSC,
                         client_id: str = "_",
                         page: int = 0,
                         page_size: int = 100) -> dict:
        path = "/v1/dataservice/tag/lp-pairs/"
        query_params = dict(id=client_id,
                            chain=locator.value,
                            pageNum=page,
                            pageSize=page_size)
        if org_id is not None:
            query_params['orgID'] = org_id
        if arbitrage_type is not None:
            query_params['arbitrageType'] = arbitrage_type.value
        if start_time is not None:
            query_params['startTime'] = start_time
        if end_time is not None:
            query_params['endTime'] = end_time
        query = urlencode(query_params)
        url = urlunsplit((self.scheme, self.host + ":" + str(self.port), path, query, ""))
        response = asyncio.run(self.__request(url))
        return response

    def get_tag_transaction(self,
                            from_address: str = None,
                            to_address: str = None,
                            arbitrage_type: ArbitrageType = None,
                            taxed: bool = None,
                            block_number_start: int = None,
                            block_number_end: int = None,
                            block_timestamp_start: int = None,
                            block_timestamp_end: int = None,
                            locator: Locator = Locator.BSC,
                            client_id: str = "_",
                            page: int = 0,
                            page_size: int = 100) -> dict:
        path = "/v1/dataservice/tag/transaction/"
        query_params = dict(id=client_id,
                            chain=locator.value,
                            pageNum=page,
                            pageSize=page_size)
        if from_address is not None:
            query_params['fromAddress'] = from_address
        if to_address is not None:
            query_params['toAddress'] = to_address
        if arbitrage_type is not None:
            query_params['arbitrageType'] = arbitrage_type.value
        if taxed is not None:
            query_params['taxed'] = "true" if taxed else "false"
        if block_number_start is not None:
            query_params['blockStart'] = block_number_start
        if block_number_end is not None:
            query_params['blockEnd'] = block_number_end
        if block_timestamp_start is not None:
            query_params['startTime'] = block_timestamp_start
        if block_timestamp_end is not None:
            query_params['endTime'] = block_timestamp_end
        query = ""
        data = json.dumps(query_params)
        url = urlunsplit((self.scheme, self.host + ":" + str(self.port), path, query, ""))
        response = asyncio.run(self.__request(url, method="post", data=data))
        return self.__fix_get_transactions_by_address_response(response)

# if __name__ == '__main__':
    # pass
    # data = Client().get(Locator.BINANCE, Category.KLINE_1Min,
    #                     "ETHUSDT", "2020-12-01", "2020-12-10")
    # for line in data:
    #     print(line)

    # data = Client().get(Locator.ANYSWAP, Category.CROSSCHAIN_TRANSFER,
    #                     "ALL", "2020-12-01", "2020-12-02")
    # for line in data:
    #     print(line)

    # data = Client().get_transaction_by_hash(
    #     tx_hash="0x97896e5b40b4ef51ec0c328a47388334e5818d2bd004bbd751da35d6b22a410e")
    # print(data)

    # data = Client().get_transactions_by_address(address="0x6d4851eaf458d0fdae1599b1241915f878c0f539")
    # print(data)

    # data = Client().get_token_transfers_by_address(address="0x06dbc4fe79e2541b03fe4731b2579c0b7f46f099", last=True)
    # print(data)

    # data = Client().get_transactions_by_block_number(9137246)
    # print(data)

    # data = Client().get_tick()
    # print(data)

    # data = Client(port=8081).get_tag_lp()
    # print(data)

    # data = Client(port=8081).get_tag_lp_pairs()
    # print(data)

    # data = Client(port=8081).get_tag_transaction()
    # print(data)