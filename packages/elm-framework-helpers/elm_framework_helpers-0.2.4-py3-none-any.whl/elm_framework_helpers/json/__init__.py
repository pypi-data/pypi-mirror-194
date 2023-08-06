from decimal import Decimal
from typing import Any
import orjson


def default(obj: Any):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError


def dumps(s: Any):
    return orjson.dumps(s, default=default)
