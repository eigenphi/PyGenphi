import datetime
import json
import uuid
from datetime import timedelta
import asyncio
import aiohttp
import os


class Client(object):

    domain = 'http://35.74.116.215/'

    def __init__(self):
        pass

    def set_dev_server(self, server: str):
        self.domain = server

    def make_url(self, locator, symbol, category, date):
        # http://127.0.0.1/kline/binance_main/ETHUSDT-2017-12-23.jsonl
        # http://127.0.0.1/crosschain/anyswap/ALL-ALL.jsonl

        url = category.value + '/' + locator.value + '/' + symbol.upper() + '-' + date + '.jsonl'
        return url

    async def job(self, session, url):
        # 声明为异步函数
        name = url.replace('%23', '-')
        full_name = os.path.join('.data', name)

        url = self.domain + url

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
        full_name = os.path.join('.data/', req_id+'.jsonl')
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


# if __name__ == '__main__':
#     pass
    # data = Client().get(Locator.BINANCE, Category.KLINE_1Min,
    #                     "ETHUSDT", "2020-12-01", "2020-12-10")
    # for line in data:
    #     print(line)

    # data = Client().get(Locator.ANYSWAP, Category.CROSSCHAIN_TRANSFER,
    #                     "ALL", "2020-12-01", "2020-12-02")
    # for line in data:
    #     print(line)
