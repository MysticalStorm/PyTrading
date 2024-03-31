from trading.interface import Price
from datetime import datetime as datetype


class BinancePrice(Price):
    @classmethod
    def from_json(cls, json):
        value = json['price']
        return cls(value=value, date=datetype.now())

    def __init__(self, value: float = 0.0, date: datetype = None):
        self._value = value
        self._date = date if date is not None else datetype.now()

    @property
    def value(self) -> float:
        return self._value

    @property
    def date(self) -> datetype:
        return self._date
