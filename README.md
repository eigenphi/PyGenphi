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
pipenv install PyGenphi==0.2.13
```

Note: run command `pipenv install PyGenphi==0.2.13` within existing `PyGenphiDemo` directory with lower version of PyGenphi will auto upgrade PyGenphi to v0.2.13

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

To fix this error, you may need install library `nest_asyncio` with command:

```python
pipenv install nest_asyncio
```

Then use it before PyGenphi lib:

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

### Candlestick chart data fetch

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


### Cross-chain bridge transfer data fetch

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

## dataservice APIs

Note: constructor of class `Client` now support params `scheme` `host` `port`, `Client()` will connect to URL with prefix `http://127.0.0.1:80/`, and `Client(scheme='https', host='192.168.1.1', port=8081)` will connect to URL with prefix `https://192.168.1.1:8081/`

### `client.get_transaction_by_hash`

#### demo

```python
from PyGenphi import *

if __name__ == '__main__':

    client = Client()
    result = client.get_transaction_by_hash(tx_hash="0x97896e5b40b4ef51ec0c328a47388334e5818d2bd004bbd751da35d6b22a410e")
    print(result)
```

#### params

| param       | type      | required | default       | note             |
|-------------|-----------|----------|---------------|------------------|
| `client_id` | `str`     | ×        | `_`           |                  |
| `locator`   | `Locator` | ×        | `Locator.BSC` | block chain      |
| `tx_hash`   | `str`     | √        |               | transaction hash |

### `client.get_transactions_by_address`

#### demo

```python
from PyGenphi import *

if __name__ == '__main__':

    client = Client()
    result = client.get_transactions_by_address(address="0x6d4851eaf458d0fdae1599b1241915f878c0f539")
    print(result)
```

#### params

| param                   | type          | required | default           | note                                               |
|-------------------------|---------------|----------|-------------------|----------------------------------------------------|
| `client_id`             | `str`         | ×        | `_`               |                                                    |
| `locator`               | `Locator`     | ×        | `Locator.BSC`     | block chain                                        |
| `address`               | `str`         | √        |                   |                                                    |
| `mode`                  | `AddressMode` | ×        | `AddressMode.ALL` | other values: `AddressMode.FROM`, `AddressMode.TO` |
| `first`                 | `bool`        | ×        | `False`           |                                                    |
| `last`                  | `bool`        | ×        | `False`           |                                                    |
| `block_number_start`    | `int`         | ×        | `None`            |                                                    |
| `block_number_end`      | `int`         | ×        | `None`            |                                                    |
| `block_timestamp_start` | `int`         | ×        | `None`            |                                                    |
| `block_timestamp_end`   | `int`         | ×        | `None`            |                                                    |

### `client.get_transactions_by_block_number`

#### demo

```python
from PyGenphi import *

if __name__ == '__main__':

    client = Client()
    result = client.get_transactions_by_block_number(block_number=9000000)
    print(result)
```

#### params

| param          | type      | required | default       | note        |
|----------------|-----------|----------|---------------|-------------|
| `client_id`    | `str`     | ×        | `_`           |             |
| `locator`      | `Locator` | ×        | `Locator.BSC` | block chain |
| `block_number` | `int`     | √        |               |             |

### `client.get_token_transfers_by_address`

#### demo

```python
from PyGenphi import *

if __name__ == '__main__':

    client = Client()
    result = client.get_token_transfers_by_address(address="0x06dbc4fe79e2541b03fe4731b2579c0b7f46f099", last=True)
    print(result)
```

#### params

| param                   | type          | required | default           | note                                               |
|-------------------------|---------------|----------|-------------------|----------------------------------------------------|
| `client_id`             | `str`         | ×        | `_`               |                                                    |
| `locator`               | `Locator`     | ×        | `Locator.BSC`     | block chain                                        |
| `address`               | `str`         | √        |                   |                                                    |
| `mode`                  | `AddressMode` | ×        | `AddressMode.ALL` | other values: `AddressMode.FROM`, `AddressMode.TO` |
| `first`                 | `bool`        | ×        | `False`           |                                                    |
| `last`                  | `bool`        | ×        | `False`           |                                                    |
| `block_number_start`    | `int`         | ×        | `None`            |                                                    |
| `block_number_end`      | `int`         | ×        | `None`            |                                                    |
| `block_timestamp_start` | `int`         | ×        | `None`            |                                                    |
| `block_timestamp_end`   | `int`         | ×        | `None`            |                                                    |
