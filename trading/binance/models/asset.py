from trading.interface import Asset, Price
from .price import BinancePrice


class BinanceAsset(Asset):

    @classmethod
    def from_json(cls, json):
        name = json['symbol']
        return cls(name=name, price=BinancePrice.from_json(json))

    def __init__(self, name: str, available_balance: str = "0", locked: str = None, price: BinancePrice = None):
        self._name = name
        self._available_balance = available_balance
        self._locked = locked
        self._price = price

    @property
    def name(self) -> str:
        return self._name

    @property
    def available_balance(self) -> str:
        return self._available_balance

    @property
    def locked(self) -> str:
        return self._locked

    @property
    def price(self) -> Price:
        return self._price
