from PyGenphi import *
import uuid

if __name__ == '__main__':
    list = Client().get(
        Locator.BINANCE,
        Category.KLINE_1Min,
        "BTCUSDT",
        "2017-12-01",
        "2017-12-10",
        str(uuid.uuid4())
    )
    for l in list:
        print(l)
