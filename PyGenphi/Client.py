import datetime
from datetime import timedelta
import asyncio
import aiohttp
import os


class Client(object):

    domain = 'http://127.0.0.1/'

    def __init__(self):
        pass

    def set_dev_server(self, server: str):
        self.domain = server

    def make_url(self, locator, symbol, date):
        # http://127.0.0.1/binance%23main-ETHUSDT-2017-12-23.json
        url = locator.value + '-' + symbol.upper() + '-' + date + '.jsonl'
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
            print("ALL RESULTS:" + str(all_results))

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

    def get(self, locator, category, symbol: str, start: str, end: str, req_id: str) -> list:

        delta_1d = timedelta(days=1)
        start_datetime = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_datetime = datetime.datetime.strptime(end, "%Y-%m-%d")
        delta = end_datetime - start_datetime
        start = start_datetime
        i = 1

        url_list = [self.make_url(locator, symbol, start.strftime("%Y-%m-%d"))]
        while i <= delta.days:
            start = start + delta_1d
            url_list.append(self.make_url(locator, symbol, start.strftime("%Y-%m-%d")))
            i += 1

        loop = asyncio.get_event_loop()
        Client.__mkdir__('.data')
        loop.run_until_complete(self.download(loop, url_list))
        return self.merge_file(url_list, req_id)


