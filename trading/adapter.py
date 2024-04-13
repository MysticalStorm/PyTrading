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
        self.subscriptions = []
        self.platform = platform
        self.db = db

    async def tickers(self):
        return await self.platform.all_tickers

    async def subscriptions(self) -> List[str]:
        return list(self.subscriptions)

    async def subscribe(self, ticker) -> AsyncGenerator[KLine, None]:
        self.subscriptions.append(ticker)
        return self.platform.subscribe(self.subscriptions)

    async def unsubscribe(self, ticker):
        self.subscriptions.remove(ticker)
        await asyncio.sleep(0.1)
        print("Unsubscribing", ticker)

