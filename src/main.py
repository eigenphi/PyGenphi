# import pandas as pd
# import numpy as np
from asyncio import get_event_loop

from category import Category
from locator import Locator
from sdk import PyGenphi


async def load_data():
    return await PyGenphi().get(
        Locator.BINANCE,
        Category.KLINE_1Min,
        "BTCUSDT",
        "2020-12-01 06:15:00", "2020-12-10 23:59:00")


# def pandas_demo(data: list):
#     df = pd.DataFrame(data=data)
#     print(df)


# def numpy_demo(data: list):
#     open_price_list = list(map(lambda x: eval(x['open']), data))
#     print("平均值为: ", np.mean(open_price_list))
#     print("方差为: ", np.var(open_price_list))
#     print("标准差为: ", np.std(open_price_list, ddof=1))


if __name__ == '__main__':
    PyGenphi().get(
        Locator.BINANCE, Category.KLINE_1Min,
        "BTCUSDT", "2017-12-01 06:15:00", "2017-12-10 23:59:00")
    # data = get_event_loop().run_until_complete(load_data())
    # numpy_demo(data)
    # pandas_demo(data)
