from typing import List

from .interface import *
import asyncio
from database.core import Database
from datetime import datetime, timedelta
from .algorithm.core import calculate_rsi, rsi_tradingview, alt_calculate_rsi
from decimal import Decimal


class TradingManager:
    def __init__(self, platform: Platform, db: Database):
        self.subscriptions = {}
        self.platform = platform
        self.db = db

    async def tickers(self):
        return await self.platform.all_tickers

    async def klines(self) -> [KLine]:
        return await self.platform.klines

    async def calculate_rsi_for_symbol(self, symbol: str) -> Decimal:
        # Get the last 14 klines for the given symbol
        end_date = int(datetime.timestamp(datetime.now()))
        start_date = int((datetime.now() - timedelta(minutes=14)).timestamp())
        last_14_klines = await self.platform.get_klines(
            symbol=symbol,
            start_date=str(start_date),
            end_date=str(end_date),
            interval='1m',
            limit=100
        )

        # Print the dates of the klines in a human-readable format
        for kline in last_14_klines:
            date = datetime.fromtimestamp(kline.kline_start_time / 1000).strftime('%Y-%m-%d %H:%M:%S')
            print(f"KLine date: {date} Open {kline.open_price} Close {kline.close_price}")

        import pandas as pd
        d = {'close': [kline.close_price for kline in last_14_klines]}
        d = pd.DataFrame(data=d)

        rsi = calculate_rsi(closes=[kline.close_price for kline in last_14_klines])
        alt_rsi = alt_calculate_rsi([kline.close_price for kline in last_14_klines])
        print(f"My RSI: {rsi} TradingRSI: {rsi_tradingview(d)[-1]} alt:{alt_rsi}")
        return rsi

    async def subscriptions(self) -> List[str]:
        return list(self.subscriptions.keys())

    async def subscribe(self, ticker):
        await self.platform.tokens
        task = asyncio.create_task(self.platform.subscribe(ticker=ticker))
        self.subscriptions[ticker] = task

    async def unsubscribe(self, ticker):
        if ticker in self.subscriptions:
            task = self.subscriptions[ticker]
            task.cancel()
            del self.subscriptions[ticker]
