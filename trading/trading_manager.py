from .interface import *
import asyncio
from database.core import Database


class TradingManager:
    def __init__(self, platform: Platform, db: Database):
        self.subscriptions = {}
        self.platform = platform
        self.db = db

    async def tickers(self):
        return await self.platform.all_tickers

    async def klines(self) -> [KLine]:
        return await self.platform.klines

    async def subscribe(self, ticker):
        task = asyncio.create_task(self.platform.subscribe(ticker=ticker))
        self.subscriptions[ticker] = task

    async def unsubscribe(self, ticker):
        if ticker in self.subscriptions:
            task = self.subscriptions[ticker]
            task.cancel()
            del self.subscriptions[ticker]