# PyGenphi
Standard Datasource of Quant Trading

Example code:

```python
from PyGenphi import *
import uuid

if __name__ == '__main__':
    data = Client().get(Locator.BINANCE, Category.KLINE_1Min, 
                        "ETHUSDT", "2017-12-01", "2017-12-10", str(uuid.uuid4()))
    for line in data:
        print(line)
```

current symbol list:
- AAVEUSDT
- ADAUSDT
- ATOMUSDT
- BCHUSDT
- BNBUSDT
- BTCUSDT
- DASHUSDT
- DOGEUSDT
- DOTUSDT
- EOSUSDT
- ETCUSDT
- ETHUSDT
- FILUSDT
- LINKUSDT
- LTCUSDT
- MATICUSDT
- NEOUSDT
- ONEUSDT
- QTUMUSDT
- SHIBUSDT
- SNXUSDT
- SOLUSDT
- SUSHIUSDT
- TRXUSDT
- UNIUSDT
- VETUSDT
- XLMUSDT
- XRPUSDT
- YFIUSDT
- ZECUSDT