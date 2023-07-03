from abc import ABC, abstractmethod


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

    @abstractmethod
    def __init__(self, name: str, available_balance: str, locked: str):
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
    def subscribe(self):
        pass
