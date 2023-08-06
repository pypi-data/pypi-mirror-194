from decimal import Decimal
from typing import TypedDict, NamedTuple

OrderbookEntry = tuple[float, float]

class Orderbook(TypedDict):
    asks: list[OrderbookEntry]
    bids: list[OrderbookEntry]
    symbol: str
    timestamp: int
    datetime: str
    nonce: str

