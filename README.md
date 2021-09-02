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
pipenv install PyGenphi==0.7.1
```

Note: run command `pipenv install PyGenphi==0.7.1` within existing `PyGenphiDemo` directory with lower version of PyGenphi will auto upgrade PyGenphi to v0.7.1

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

Note: constructor of class `Client` now support optional parameters `scheme` `host` `port` `api_key`, `Client()` will connect to URL with prefix `http://127.0.0.1:80/`, and `Client(scheme='https', host='192.168.1.1', port=8081, api_key='<your_api_key>')` will connect to URL with prefix `https://192.168.1.1:8081/` with HTTP header `APIKey` for authentication

### common request parameters

#### Enum `Locator`

- `Locator.BSC`
- `Locator.ANYSWAP`
- `Locator.BINANCE`

#### Enum `ArbitrageType`

- `ArbitrageType.ALL_ARBITRAGE`
- `ArbitrageType.TWIN_ARBITRAGE`
- `ArbitrageType.TRIANGLE_ARBITRAGE`
- `ArbitrageType.MULTIPLE_ARBITRAGE`
- `ArbitrageType.NO_ARBITRAGE`
- `ArbitrageType.UNKNOWN`

### common response data structure

#### transaction

| field                      | type    | meaning                                                           | note              |
|----------------------------|---------|-------------------------------------------------------------------|-------------------|
| `locator`                  | str     | blockchain network                                                |                   |
| `transactionHash`          | str     | transaction hash                                                  |                   |
| `transactionIndex`         | int     | transaction index(in block)                                       |                   |
| `nonce`                    | int     | the number of transactions made by the sender prior to this one   |                   |
| `transactionReceiptStatus` | bool    | transaction receipt status, `True` for success, `False` for faild |                   |
| `errCode`                  | str     | error code when transaction faild                                 | NOT implement yet |
| `blockNumber`              | int     | block number                                                      |                   |
| `blockHash`                | str     | block hash                                                        |                   |
| `blockTimestamp`           | int     | Unix time(in second)                                              |                   |
| `fromAddress`              | str     | from address                                                      |                   |
| `toAddress`                | str     | to address                                                        |                   |
| `transactionValue`         | Decimal | transaction value(amount)                                         |                   |
| `gasUsed`                  | int     | gas used                                                          |                   |
| `gasPrice`                 | int     | gas price                                                         |                   |
| `input`                    | str     | input parameters                                                  |                   |
| `logs`                     | list    | logs of transaction receipt                                       |                   |
| `logs[n]`                  | dict    | log of transaction receipt                                        | see `event log`   |
| `labels`                   | list    | labels of current transaction                                     | NOT implement yet |
| `labels[n]`                | str     | label of current transaction                                      | NOT implement yet |

#### event log

| field              | type | meaning                                                                 | note                   |
|--------------------|------|-------------------------------------------------------------------------|------------------------|
| `locator`          | str  | blockchain network                                                      |                        |
| `transactionHash`  | str  | transaction hash                                                        |                        |
| `transactionIndex` | int  | transaction index(in block)                                             |                        |
| `blockNumber`      | int  | block number                                                            |                        |
| `blockHash`        | str  | block hash                                                              |                        |
| `blockTimestamp`   | int  | Unix time(in second)                                                    |                        |
| `logIndex`         | int  | log index(in block)                                                     |                        |
| `address`          | str  | address that generate current log                                       |                        |
| `topic0`           | str  | method signature of current log                                         |                        |
| `topic1`           | str  | indexed param 1 of current log                                          |                        |
| `topic2`           | str  | indexed param 2 of current log                                          |                        |
| `topic3`           | str  | indexed param 3 of current log                                          |                        |
| `data`             | str  | more param data                                                         |                        |
| `dataParsed`       | dict | topics and data parsed by method signature                              | see `event log parsed` |
| `category`         | str  | method name if parsed else same to topic0                               |                        |
| `removed`          | bool | `True`: log valid, `False`: log was removed due to chain reorganization |                        |

##### event log parsed

###### transfer

| field             | type    | meaning               | note              |
|-------------------|---------|-----------------------|-------------------|
| `category`        | str     | value is `"transfer"` |                   |
| `tokenAddress`    | str     | address of token      |                   |
| `token`           | dict    | token info            | see `token` below |
| `senderAddress`   | str     | address of sender     |                   |
| `receiverAddress` | str     | address of receiver   |                   |
| `tokenAmount`     | Decimal | transfer amount       |                   |

###### swap

| field         | type    | meaning                         | note              |
|---------------|---------|---------------------------------|-------------------|
| `category`    | str     | value is `"swap"`               |                   |
| `lpAddress`   | str     | address of liquid pair contract |                   |
| `lp`          | dict    | liquid pair info                | see `lp` below    |
| `token0`      | dict    | token0 info                     | see `token` below |
| `token1`      | dict    | token1 info                     | see `token` below |
| `fromAddress` | str     | address of sender               |                   |
| `toAddress`   | str     | address of receiver             |                   |
| `amount0In`   | Decimal | input amount of token0          |                   |
| `amount1In`   | Decimal | input amount of token1          |                   |
| `amount0Out`  | Decimal | output amount of token0         |                   |
| `amount1Out`  | Decimal | output amount of token1         |                   |

###### sync

| field       | type    | meaning                         | note              |
|-------------|---------|---------------------------------|-------------------|
| `category`  | str     | value is `"sync"`               |                   |
| `lpAddress` | str     | address of liquid pair contract |                   |
| `lp`        | dict    | liquid pair info                | see `lp` below    |
| `token0`    | dict    | token0 info                     | see `token` below |
| `token1`    | dict    | token1 info                     | see `token` below |
| `reserve0`  | Decimal | reserve of token0               |                   |
| `reserve1`  | Decimal | reserve of token1               |                   |

##### lp

| field    | type | meaning                          | note |
|----------|------|----------------------------------|------|
| `token0` | str  | address of token0 of liquid pair |      |
| `token1` | str  | address of token1 of liquid pair |      |
| `symbol` | str  | symbol of liquid pair            |      |

##### token

| field      | type | meaning            | note |
|------------|------|--------------------|------|
| `symbol`   | str  | symbol of token0   |      |
| `decimals` | int  | decimals of token0 |      |

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

#### result

response body is a JSON string, more details:

| field    | type | meaning                                      | note                                                    |
|----------|------|----------------------------------------------|---------------------------------------------------------|
| `domain` | str  | URI of current API                           |                                                         |
| `id`     | str  | client ID                                    |                                                         |
| `result` | dict | transaction, `None` if transaction NOT exist | see `transaction` in [common response data structure][] |

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

#### result

| field       | type | meaning            | note                                                    |
|-------------|------|--------------------|---------------------------------------------------------|
| `domain`    | str  | URI of current API |                                                         |
| `id`        | str  | client ID          |                                                         |
| `result`    | list | transaction list   |                                                         |
| `result[n]` | dict | transaction        | see `transaction` in [common response data structure][] |

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

#### result

| field       | type | meaning            | note                                                    |
|-------------|------|--------------------|---------------------------------------------------------|
| `domain`    | str  | URI of current API |                                                         |
| `id`        | str  | client ID          |                                                         |
| `result`    | list | transaction list   |                                                         |
| `result[n]` | dict | transaction        | see `transaction` in [common response data structure][] |

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

#### result

| field       | type | meaning            | note                                                  |
|-------------|------|--------------------|-------------------------------------------------------|
| `domain`    | str  | URI of current API |                                                       |
| `id`        | str  | client ID          |                                                       |
| `result`    | list | event log list     |                                                       |
| `result[n]` | dict | event log          | see `event log` in [common response data structure][] |

### `client.get_tick`

#### demo

```python
from PyGenphi import *

if __name__ == '__main__':

    client = Client()
    result = client.get_tick()
    print(result)
```

#### params

| param                   | type      | required | default       | note                         |
|-------------------------|-----------|----------|---------------|------------------------------|
| `client_id`             | `str`     | ×        | `_`           |                              |
| `locator`               | `Locator` | ×        | `Locator.BSC` | block chain                  |
| `lp_addrs`              | `str`     | ×        | `None`        | multi address split with `,` |
| `block_number_start`    | `int`     | ×        | `None`        |                              |
| `block_number_end`      | `int`     | ×        | `None`        |                              |
| `block_timestamp_start` | `int`     | ×        | `None`        |                              |
| `block_timestamp_end`   | `int`     | ×        | `None`        |                              |
| `page`                  | `int`     | ×        | `0`           |                              |
| `page_size`             | `int`     | ×        | `100`         | range: [1, 100]              |

#### result

| field                          | type    | meaning            | note |
|--------------------------------|---------|--------------------|------|
| `domain`                       | str     | URI of current API |      |
| `id`                           | str     | client ID          |      |
| `result`                       | list    | tick list          |      |
| `result[n]`                    | dict    | tick               |      |
| `result[n].blockNumber`        | int     |                    |      |
| `result[n].logIndex`           | int     |                    |      |
| `result[n].transactionIndex`   | int     |                    |      |
| `result[n].transactionHash`    | str     |                    |      |
| `result[n].blockTimestamp`     | int     |                    |      |
| `result[n].localTimestamp`     | int     |                    |      |
| `result[n].lp`                 | dict    |                    |      |
| `result[n].lp.address`         | str     |                    |      |
| `result[n].lp.minLiquidity`    | str     |                    |      |
| `result[n].lp.decimals`        | int     |                    |      |
| `result[n].lp.factory`         | str     |                    |      |
| `result[n].lp.name`            | str     |                    |      |
| `result[n].lp.symbol`          | str     |                    |      |
| `result[n].lp.totalSupply`     | str     |                    |      |
| `result[n].token0`             | dict    |                    |      |
| `result[n].token0.address`     | str     |                    |      |
| `result[n].token0.symbol`      | str     |                    |      |
| `result[n].token0.decimals`    | int     |                    |      |
| `result[n].token0.name`        | str     |                    |      |
| `result[n].token0.totalSupply` | str     |                    |      |
| `result[n].token1`             | dict    |                    |      |
| `result[n].token1.address`     | str     |                    |      |
| `result[n].token1.symbol`      | str     |                    |      |
| `result[n].token1.decimals`    | int     |                    |      |
| `result[n].token1.name`        | str     |                    |      |
| `result[n].token1.totalSupply` | str     |                    |      |
| `result[n].reserve0`           | Decimal |                    |      |
| `result[n].reserve1`           | Decimal |                    |      |
| `result[n].lpAddress`          | str     |                    |      |

### `client.get_previoustick`

Note: parameter `api_key` of `Client` is required for this API

#### demo

```python
from PyGenphi import *

if __name__ == '__main__':

    client = Client(api_key="<your-api-key>")
    result = client.get_previoustick(lp_addr="<lp_addr>", block_number_end=7900000, log_index=297)
    print(result)
```

#### params

| param                   | type      | required | default       | note        |
|-------------------------|-----------|----------|---------------|-------------|
| `client_id`             | `str`     | ×        | `_`           |             |
| `locator`               | `Locator` | ×        | `Locator.BSC` | block chain |
| `lp_addr`               | `str`     | √        |               |             |
| `block_number_end`      | `int`     | √        |               |             |
| `block_number_start`    | `int`     | ×        | `None`        |             |
| `log_index`             | `int`     | √        |               |             |
| `block_timestamp_start` | `int`     | ×        | `None`        |             |
| `block_timestamp_end`   | `int`     | ×        | `None`        |             |

#### result

| field                     | type    | meaning            | note |
|---------------------------|---------|--------------------|------|
| `domain`                  | str     | URI of current API |      |
| `id`                      | str     | client ID          |      |
| `result`                  | dict    | tick               |      |
| `result.blockNumber`      | int     |                    |      |
| `result.logIndex`         | int     |                    |      |
| `result.transactionIndex` | int     |                    |      |
| `result.transactionHash`  | str     |                    |      |
| `result.blockTimestamp`   | int     |                    |      |
| `result.taggedMillis`     | int     |                    |      |
| `result.lp`               | dict    |                    |      |
| `result.lp.address`       | str     |                    |      |
| `result.lp.minLiquidity`  | str     |                    |      |
| `result.lp.decimals`      | int     |                    |      |
| `result.lp.factory`       | str     |                    |      |
| `result.lp.name`          | str     |                    |      |
| `result.lp.symbol`        | str     |                    |      |
| `result.token0`           | dict    |                    |      |
| `result.token0.address`   | str     |                    |      |
| `result.token0.symbol`    | str     |                    |      |
| `result.token0.decimals`  | int     |                    |      |
| `result.token0.name`      | str     |                    |      |
| `result.token1`           | dict    |                    |      |
| `result.token1.address`   | str     |                    |      |
| `result.token1.symbol`    | str     |                    |      |
| `result.token1.decimals`  | int     |                    |      |
| `result.token1.name`      | str     |                    |      |
| `result.reserve0`         | Decimal |                    |      |
| `result.reserve1`         | Decimal |                    |      |
| `result.lpAddress`        | str     |                    |      |

### `client.get_tag_lp`

Note: parameter `api_key` of `Client` is required for this API

#### demo

```python
from PyGenphi import *

if __name__ == '__main__':

    client = Client(api_key="<your-api-key>")
    result = client.get_tag_lp()
    print(result)
```

#### params

| param        | type      | required | default       | note                   |
|--------------|-----------|----------|---------------|------------------------|
| `client_id`  | `str`     | ×        | `_`           |                        |
| `locator`    | `Locator` | ×        | `Locator.BSC` | block chain            |
| `lp_address` | `str`     | ×        |               |                        |
| `is_secure`  | `bool`    | ×        |               |                        |
| `start_time` | `int`     | ×        |               | LP used time in millis |
| `end_time`   | `int`     | ×        |               | LP used time in millis |
| `page`       | `int`     | ×        | `0`           |                        |
| `page_size`  | `int`     | ×        | `100`         | range: [1, 100]        |

#### result

| field                          | type | meaning               | note |
|--------------------------------|------|-----------------------|------|
| `domain`                       | str  | URI of current API    |      |
| `id`                           | str  | client ID             |      |
| `result`                       | list | tag LP info list      |      |
| `result[n]`                    | dict | tag LP info           |      |
| `result[n].chain`              | str  | block chain of tag LP |      |
| `result[n].name`               | str  | tag LP name           |      |
| `result[n].symbol`             | str  | tag LP symbol         |      |
| `result[n].decimals`           | int  |                       |      |
| `result[n].token0Address`      | str  |                       |      |
| `result[n].token1Address`      | str  |                       |      |
| `result[n].minLiquidity`       | str  |                       |      |
| `result[n].isSecure`           | bool |                       |      |
| `result[n].totalSupply`        | str  |                       |      |
| `result[n].token0`             | dict |                       |      |
| `result[n].token0.address`     | str  |                       |      |
| `result[n].token0.name`        | str  |                       |      |
| `result[n].token0.symbol`      | str  |                       |      |
| `result[n].token0.decimals`    | int  |                       |      |
| `result[n].token0.totalSupply` | str  |                       |      |
| `result[n].token1`             | dict |                       |      |
| `result[n].token1.address`     | str  |                       |      |
| `result[n].token1.name`        | str  |                       |      |
| `result[n].token1.symbol`      | str  |                       |      |
| `result[n].token1.decimals`    | int  |                       |      |
| `result[n].token1.totalSupply` | str  |                       |      |
| `result[n].lpAddress`          | str  |                       |      |
| `result[n].factory`            | str  |                       |      |

### `client.get_tag_lp_pairs`

Note: parameter `api_key` of `Client` is required for this API

#### demo

```python
from PyGenphi import *

if __name__ == '__main__':

    client = Client(api_key="<your-api-key>")
    result = client.get_tag_lp_pairs()
    print(result)
```

#### params

| param            | type            | required | default       | note                                                      |
|------------------|-----------------|----------|---------------|-----------------------------------------------------------|
| `client_id`      | `str`           | ×        | `_`           |                                                           |
| `locator`        | `Locator`       | ×        | `Locator.BSC` | block chain                                               |
| `org_id`         | `str`           | ×        |               |                                                           |
| `arbitrage_type` | `ArbitrageType` | ×        | `None`        | see Enum `ArbitrageType` in [common request parameters][] |
| `start_time`     | `int`           | ×        |               | LP Pairs used time in millis                              |
| `end_time`       | `int`           | ×        |               | LP Pairs used time in millis                              |
| `page`           | `int`           | ×        | `0`           |                                                           |
| `page_size`      | `int`           | ×        | `100`         | range: [1, 100]                                           |

#### result

| field                     | type | meaning               | note |
|---------------------------|------|-----------------------|------|
| `domain`                  | str  | URI of current API    |      |
| `id`                      | str  | client ID             |      |
| `result`                  | list | tag LP Pair info list |      |
| `result[n]`               | dict | tag LP Pair info      |      |
| `result[n].chain`         | str  | block chain of tag LP |      |
| `result[n].orgID`         | str  |                       |      |
| `result[n].facotryCombo`  | str  |                       |      |
| `result[n].decimals`      | int  |                       |      |
| `result[n].arbitrageType` | str  |                       |      |
| `result[n].createTime`    | int  |                       |      |
| `result[n].updateTime`    | int  |                       |      |
| `result[n].lpCombo`       | str  |                       |      |

### `client.get_tag_transaction`

Note: parameter `api_key` of `Client` is required for this API

#### demo

```python
from PyGenphi import *

if __name__ == '__main__':

    client = Client(api_key="<your-api-key>")
    result = client.get_tag_transaction()
    print(result)
```

#### params

| param                   | type            | required | default       | note                                                      |
|-------------------------|-----------------|----------|---------------|-----------------------------------------------------------|
| `client_id`             | `str`           | ×        | `_`           |                                                           |
| `locator`               | `Locator`       | ×        | `Locator.BSC` | block chain                                               |
| `from_address`          | `str`           | ×        | `None`        |                                                           |
| `to_address`            | `str`           | ×        | `None`        |                                                           |
| `arbitrage_type`        | `ArbitrageType` | ×        | `None`        | see Enum `ArbitrageType` in [common request parameters][] |
| `taxed`                 | `bool`          | ×        | `None`        |                                                           |
| `block_number_start`    | `int`           | ×        | `None`        |                                                           |
| `block_number_end`      | `int`           | ×        | `None`        |                                                           |
| `block_timestamp_start` | `int`           | ×        | `None`        |                                                           |
| `block_timestamp_end`   | `int`           | ×        | `None`        |                                                           |
| `page`                  | `int`           | ×        | `0`           |                                                           |
| `page_size`             | `int`           | ×        | `100`         | range: [1, 100]                                           |

#### result

| field       | type | meaning            | note                                                    |
|-------------|------|--------------------|---------------------------------------------------------|
| `domain`    | str  | URI of current API |                                                         |
| `id`        | str  | client ID          |                                                         |
| `result`    | list | transaction list   |                                                         |
| `result[n]` | dict | transaction        | see `transaction` in [common response data structure][] |
