# PyGenphi
Standard Datasource of DeFi research

## create a new Python project using PyGenphi
```python
mkdir PyGenphiDemo
cd PyGenphiDemo

git init

pipenv install --dev
# activate venv
pipenv shell
# install PyGenphi
pipenv install PyGenphi==0.1.8
```

### IMPORTANT NOTE FOR IPython(Jupter/anaconda3) users:

You may get an error report like:
```python
~/opt/anaconda3/lib/python3.7/asyncio/base_events.py in run_forever(self)
    519         self._check_closed()
    520         if self.is_running():
--> 521             raise RuntimeError('This event loop is already running')
    522         if events._get_running_loop() is not None:
    523             raise RuntimeError(

RuntimeError: This event loop is already running
```

To fix this error, you may need to use a nest_asyncio lib: 
```python
pipenv install nest_asyncio
```
Then use it before PyGenphi lib

```python
import nest_asyncio
from PyGenphi import *

nest_asyncio.apply()
if __name__ == '__main__':
    
    data = Client().get(
        Locator.BINANCE,        # Data location
        Category.KLINE_1Min,    # Data category
        "ETHUSDT",              # symbol or token, default value="ALL"
        "2020-12-01",           # start date of data, default value="ALL"
        "2020-12-10",            # end date of data, default value="ALL"
        "1"                     # request id used to generate cache file, default value is a random uuid
    )
```


## Example code:

### Candlestick chart data fetch:
```python
from PyGenphi import *
import uuid

if __name__ == '__main__':
    
    data = Client().get(
        Locator.BINANCE,        # Data location
        Category.KLINE_1Min,    # Data category
        "ETHUSDT",              # symbol or token, default value="ALL"
        "2020-12-01",           # start date of data, default value="ALL"
        "2020-12-10",            # end date of data, default value="ALL"
        "1"                     # request id used to generate cache file, default value is a random uuid
    )
    
    for line in data:
        print(line)
```

symbol list for Candlestick chart supported:
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


### Cross-chain bridge transfer data fetch:

```python
from PyGenphi import *

if __name__ == '__main__':
    
    data = Client().get(
        Locator.ANYSWAP, 
        Category.CROSSCHAIN_TRANSFER,
        "ALL", 
        "2020-12-01", 
        "2020-12-02"
    )
    for line in data:
        print(line)
```

- location supported: Locator.ANYSWAP
- data span: 2020-08-17  ~  2021-06-23 (maybe change anytime)
