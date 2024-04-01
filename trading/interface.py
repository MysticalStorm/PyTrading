from abc import ABC, abstractmethod
from .models.kline import KLine
from datetime import date
from typing import AsyncGenerator


class Price(ABC):
    @property
    @abstractmethod
    def value(self) -> float:
        pass

    @property
    @abstractmethod
    def date(self) -> date:
        pass


class Asset(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def available_balance(self) -> str:
        pass

    @property
    @abstractmethod
    def locked(self) -> str:
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        pass

    @abstractmethod
    def __init__(self, name: str, available_balance: str, locked: str, price: float):
        pass


class Balance(ABC):
    @property
    @abstractmethod
    def assets(self) -> [Asset]:
        pass

    @abstractmethod
    def __init__(self, assets: [Asset]):
        pass


class Platform(ABC):
    @property
    @abstractmethod
    async def klines(self) -> [KLine]:
        pass

    @property
    @abstractmethod
    async def balance(self) -> Balance:
        pass

    @property
    @abstractmethod
    async def all_tickers(self) -> [Asset]:
        pass

    @property
    @abstractmethod
    async def tokens(self) -> [Asset]:
        pass

    @abstractmethod
    def subscribe(self, ticker: str) -> AsyncGenerator[KLine, None]:
        pass

    @abstractmethod
    async def get_klines(self, symbol: str, start_date: str, end_date: str, interval: str, limit: int) -> [KLine]:
        pass
