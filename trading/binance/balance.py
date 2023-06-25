from typing import List
from ..interface import Balance
from .asset import BinanceAsset


class BinanceBalance(Balance):
    def __init__(self, assets: List[BinanceAsset]):
        self._assets = assets

    @property
    def assets(self) -> List[BinanceAsset]:
        return self._assets
