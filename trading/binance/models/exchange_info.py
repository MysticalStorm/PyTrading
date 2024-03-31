from datetime import datetime
from typing import List, Optional


class RateLimit:
    def __init__(self, rate_limit_type: str, interval: str, limit: int):
        self.rate_limit_type = rate_limit_type
        self.interval = interval
        self.limit = limit

    @classmethod
    def from_json(cls, json):
        return cls(rate_limit_type=json['rateLimitType'], interval=json['interval'], limit=json['limit'])


class Filter:
    def __init__(self, filter_type: str, **kwargs):
        self.filterType = filter_type
        self.__dict__.update(kwargs)

    @classmethod
    def from_json(cls, json):
        return cls(filter_type=json['filterType'], **json)


class Symbol:
    def __init__(self, symbol: str, status: str, base_asset: str, base_asset_precision: int,
                 quote_asset: str, quote_precision: int, order_types: List[str], iceberg_allowed: bool,
                 filters: List[Filter]):
        self.symbol = symbol
        self.status = status
        self.base_asset = base_asset
        self.base_asset_precision = base_asset_precision
        self.quote_asset = quote_asset
        self.quote_precision = quote_precision
        self.order_types = order_types
        self.iceberg_allowed = iceberg_allowed
        self.filters = filters

    @classmethod
    def from_json(cls, json):
        filters = [Filter.from_json(f) for f in json['filters']]
        return cls(symbol=json['symbol'], status=json['status'], base_asset=json['baseAsset'],
                   base_asset_precision=json['baseAssetPrecision'], quote_asset=json['quoteAsset'],
                   quote_precision=json['quotePrecision'], order_types=json['orderTypes'],
                   iceberg_allowed=json['icebergAllowed'], filters=filters)


class ExchangeInfo:
    def __init__(self, timezone: str, server_time: int, rate_limits: List[RateLimit], exchange_filters: List[dict],
                 symbols: List[Symbol]):
        self.timezone = timezone
        self.server_time = datetime.utcfromtimestamp(server_time / 1000.0)
        self.rate_limits = rate_limits
        self.exchange_filters = exchange_filters
        self.symbols = symbols

    @classmethod
    def from_json(cls, json):
        rate_limits = [RateLimit.from_json(limit) for limit in json['rateLimits']]
        symbols = [Symbol.from_json(symbol) for symbol in json['symbols']]
        return cls(timezone=json['timezone'], server_time=json['serverTime'],
                   rate_limits=rate_limits, exchange_filters=json['exchangeFilters'], symbols=symbols)
