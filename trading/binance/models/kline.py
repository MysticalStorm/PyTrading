from trading.models.kline import KLine


class BinanceKLine(KLine):
    def __init__(self, json_data):
        self._event_type = json_data['e']
        self._event_time = json_data['E']
        self._symbol = json_data['s']

        kline_data = json_data['k']
        self._kline_start_time = kline_data['t']
        self._kline_end_time = kline_data['T']
        self._kline_interval = kline_data['i']
        self._first_trade_id = kline_data['f']
        self._last_trade_id = kline_data['L']
        self._open_price = kline_data['o']
        self._close_price = kline_data['c']
        self._high_price = kline_data['h']
        self._low_price = kline_data['l']
        self._base_volume = kline_data['v']
        self._number_of_trades = kline_data['n']
        self._is_final_bar = kline_data['x']
        self._quote_asset_volume = kline_data['q']
        self._taker_buy_base_asset_volume = kline_data['V']
        self._taker_buy_quote_asset_volume = kline_data['Q']
        self._ignore = kline_data['B']

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
    def close_price(self) -> str:
        return self._close_price

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
