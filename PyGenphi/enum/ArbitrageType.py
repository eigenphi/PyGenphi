from enum import Enum


class ArbitrageType(Enum):
    ALL_ARBITRAGE = "AS000"
    TWIN_ARBITRAGE = "AS001"
    TRIANGLE_ARBITRAGE = "AS002"
    MULTIPLE_ARBITRAGE = "AS009"
    NO_ARBITRAGE = "AS098"
    UNKNOWN = "AS400"