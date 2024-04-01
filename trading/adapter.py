from typing import List

from .interface import *
import asyncio
from database.core import Database
from datetime import datetime, timedelta
from .algorithm.core import calculate_rsi, rsi_tradingview, alt_calculate_rsi
from decimal import Decimal
from typing import AsyncGenerator


class TradingManager:
    def __init__(self, platform: Platform, db: Database):
        self.subscriptions = {}
        self.platform = platform
        self.db = db

    async def tickers(self):
        return await self.platform.all_tickers

    async def klines(self) -> [KLine]:
        return await self.platform.klines

    async def subscriptions(self) -> List[str]:
        return list(self.subscriptions.keys())

    async def subscribe(self, ticker) -> AsyncGenerator[KLine, None]:
        return self.platform.subscribe(ticker)

    async def unsubscribe(self, ticker):
        if ticker in self.subscriptions:
            task = self.subscriptions[ticker]
            task.cancel()
            del self.subscriptions[ticker]
