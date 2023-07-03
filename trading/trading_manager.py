from .interface import *
import asyncio
from web.database.core import Database

class TradingManager:
    def __init__(self, platform: Platform, db: Database):
        self.subscriptions = {}
        self.platform = platform
        self.db = db

    async def subscribe(self):
        task1 = asyncio.create_task(self.platform.subscribe())
        self.subscriptions["ETHUSDT"] = task1
        await self.db.save("Subscribe MESSAGE")

    async def run(self):
        await asyncio.gather(*self.subscriptions.values())
