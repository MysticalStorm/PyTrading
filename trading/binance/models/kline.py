from trading.models.kline import KLine
import json
from decimal import Decimal


class BinanceKLine(KLine):
    def __init__(self, json_data):
        if isinstance(json_data, str):
            json_data = {}

        self._event_type = json_data.get('e', None)
        self._event_time = json_data.get('E', None)
        self._symbol = json_data.get('s', None)

        kline_data = json_data.get('k', {})
        self._kline_start_time = kline_data.get('t', None)
        self._kline_end_time = kline_data.get('T', None)
        self._kline_interval = kline_data.get('i', None)
        self._first_trade_id = kline_data.get('f', None)
        self._last_trade_id = kline_data.get('L', None)
        self._open_price = kline_data.get('o', None)
        self._close_price = kline_data.get('c', None)
        self._high_price = kline_data.get('h', None)
        self._low_price = kline_data.get('l', None)
        self._base_volume = kline_data.get('v', None)
        self._number_of_trades = kline_data.get('n', None)
        self._is_final_bar = kline_data.get('x', None)
        self._quote_asset_volume = kline_data.get('q', None)
        self._taker_buy_base_asset_volume = kline_data.get('V', None)
        self._taker_buy_quote_asset_volume = kline_data.get('Q', None)
        self._ignore = kline_data.get('B', None)

    @property
    def event_type(self) -> str:
        return self._event_type

    @property
    def event_time(self) -> int:
        return self._event_time

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def kline_start_time(self) -> int:
        return self._kline_start_time

    @property
    def kline_end_time(self) -> int:
        return self._kline_end_time

    @property
    def kline_interval(self) -> str:
        return self._kline_interval

    @property
    def first_trade_id(self) -> int:
        return self._first_trade_id

    @property
    def last_trade_id(self) -> int:
        return self._last_trade_id

    @property
    def open_price(self) -> str:
        return self._open_price

    @property
    def close_price(self) -> Decimal:
        return Decimal(self._close_price)

    @property
    def high_price(self) -> str:
        return self._high_price

    @property
    def low_price(self) -> str:
        return self._low_price

    @property
    def base_volume(self) -> str:
        return self._base_volume

    @property
    def number_of_trades(self) -> int:
        return self._number_of_trades

    @property
    def quote_asset_volume(self) -> str:
        return self._quote_asset_volume

    @property
    def taker_buy_base_asset_volume(self) -> str:
        return self._taker_buy_base_asset_volume

    @property
    def taker_buy_quote_asset_volume(self) -> str:
        return self._taker_buy_quote_asset_volume

    @property
    def is_final_bar(self) -> str:
        return self._is_final_bar

    @property
    def ignore(self) -> str:
        return self._ignore


class HistoricalKLine(BinanceKLine):
    def __init__(self, json_data):
        super().__init__(json_data)
        json_data = json.loads(json_data)

        self._kline_start_time = json_data[0]
        self._open_price = json_data[1]
        self._close_price = json_data[4]
        self._high_price = json_data[2]
        self._low_price = json_data[3]
        self._base_volume = json_data[5]
