from abc import ABC, abstractmethod
from decimal import Decimal

class KLine(ABC):
    @property
    @abstractmethod
    def event_type(self) -> str:
        pass

    @property
    @abstractmethod
    def event_time(self) -> int:
        pass

    @property
    @abstractmethod
    def symbol(self) -> str:
        pass

    @property
    @abstractmethod
    def kline_start_time(self) -> int:
        pass

    @property
    @abstractmethod
    def kline_end_time(self) -> int:
        pass

    @property
    @abstractmethod
    def kline_interval(self) -> str:
        pass

    @property
    @abstractmethod
    def first_trade_id(self) -> int:
        pass

    @property
    @abstractmethod
    def last_trade_id(self) -> int:
        pass

    @property
    @abstractmethod
    def open_price(self) -> str:
        pass

    @property
    @abstractmethod
    def close_price(self) -> Decimal:
        pass

    @property
    @abstractmethod
    def high_price(self) -> str:
        pass

    @property
    @abstractmethod
    def low_price(self) -> str:
        pass

    @property
    @abstractmethod
    def base_volume(self) -> str:
        pass

    @property
    @abstractmethod
    def number_of_trades(self) -> int:
        pass

    @property
    @abstractmethod
    def is_final_bar(self) -> bool:
        pass

    @property
    @abstractmethod
    def quote_asset_volume(self) -> str:
        pass

    @property
    @abstractmethod
    def taker_buy_base_asset_volume(self) -> str:
        pass

    @property
    @abstractmethod
    def taker_buy_quote_asset_volume(self) -> str:
        pass

    @property
    @abstractmethod
    def ignore(self) -> str:
        pass