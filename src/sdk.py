import json
import uuid
from aiohttp import ClientSession
from locator import Locator
from category import Category
import datetime
from datetime import timedelta
import asyncio
import time
import requests
import aiohttp

class PyGenphi(object):

    domain = 'http://127.0.0.1/'

    def __init__(self):
        pass

    def set_dev_server(self, server: str):
        self.domain = server

    # async def getV1(self,
    #               locator: Locator,
    #               category: Category,
    #               symbol: str,
    #               start: str, end: str) -> list:
    #     request_id = str(uuid.uuid4())
    #     request = {
    #         'jsonrpc': '2.0',
    #         'method': category.value, 'params': {
    #         "locator": locator.value,
    #         "instrument": symbol.upper(),
    #         "start": start,
    #         "end": end
    #     }, 'id': request_id}
    #     try:
    #         async with ClientSession() as session:
    #             async with session.post(self.url, json=request) as resp:
    #                 response = await resp.text()
    #                 j = json.loads(response)
    #                 if j['id'] != request_id:
    #                     raise Exception('Bad response from DataBank server');
    #                 return j['result']
    #     except Exception as ex:
    #         print(ex)

    def make_url(self, locator, symbol, date):
        # http://127.0.0.1/binance%23main-ETHUSDT-2017-12-23.json
        url = locator.value + '-' + symbol.upper() + '-' + date + '.jsonl'
        return url

    async def job(self, session, url):
        # 声明为异步函数
        name = url.replace('%23', '-')
        url = self.domain + url

        # 获得名字
        f = await session.get(url)
        # 触发到await就切换，等待get到数据
        content = await f.read()
        # 读取内容
        with open(str(name), "wb") as fout:
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
            print("ALL RESULTS:" + str(all_results))

    async def merge_file(self, url_list) -> list:
        with open('output_file.jsonl', 'w') as outfile:
            for fname in url_list:
                fname = fname.replace('%23', '-')
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

    def get(self, locator: Locator, category: Category, symbol: str, start: str, end: str) -> list:

        delta_1d = timedelta(days=1)
        start_datetime = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        delta = end_datetime - start_datetime
        start = start_datetime
        i = 1

        url_list = [self.make_url(locator, symbol, start.strftime("%Y-%m-%d"))]
        while i <= delta.days:
            start = start + delta_1d
            url_list.append(self.make_url(locator, symbol, start.strftime("%Y-%m-%d")))
            i += 1

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.download(loop, url_list))
        loop.run_until_complete(self.merge_file(url_list))


