
from decimal import Decimal
from typing import NamedTuple

class OrderbookEntry(NamedTuple):
    price: float
    volume: float

class TopPrices(NamedTuple):
    bid: Decimal
    ask: Decimal