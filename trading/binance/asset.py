from ..interface import Asset


class BinanceAsset(Asset):
    def __init__(self, name: str, available_balance: str, locked: str):
        self._name = name
        self._available_balance = available_balance
        self._locked = locked

    @property
    def name(self) -> str:
        return self._name

    @property
    def available_balance(self) -> str:
        return self._available_balance

    @property
    def locked(self) -> str:
        return self._locked
