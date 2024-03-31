from typing import List
from trading.interface import Balance
from trading.binance.models.asset import BinanceAsset


class BinanceBalance(Balance):
    def __init__(self, assets: List[BinanceAsset]):
        self._assets = assets

    @property
    def assets(self) -> List[BinanceAsset]:
        return self._assets
