from private.credentials import *
from binance.client import AsyncClient
from binance.streams import BinanceSocketManager
from ..interface import Platform
from trading.binance.models.asset import BinanceAsset
from trading.binance.models.balance import BinanceBalance
import json
import asyncio
from .models.kline import BinanceKLine, HistoricalKLine
from .models.exchange_info import ExchangeInfo
from typing import AsyncGenerator
import json
import websockets


class Binance(Platform):
    def __init__(self):
        self._balance = None
        self._async_client = AsyncClient(api_key, secret_key, testnet=False)
        self._socket_manager = BinanceSocketManager(client=self._async_client)

    @property
    async def balance(self) -> BinanceBalance:
        # Get account information
        info = await self._async_client.get_account()

        # The 'balances' field in the returned dictionary is a list of asset balances
        for asset in info['balances']:
            # Each asset is a dictionary with 'asset', 'free', and 'locked' fields
            asset_name = asset['asset']
            available_balance = asset['free']
            on_order = asset['locked']

            # print(f"Asset: {asset_name}, Available: {available_balance}, On Order: {on_order}")

            asset = BinanceAsset(name=asset_name, available_balance=available_balance, locked=on_order)
            self._balance = BinanceBalance(assets=[asset])

        return self._balance

    @property
    async def all_tickers(self) -> [BinanceAsset]:
        tickers = await self._async_client.get_all_tickers()
        return [BinanceAsset.from_json(symbol_info) for symbol_info in tickers]

    @property
    async def tokens(self) -> [BinanceAsset]:
        info_json = await self._async_client.get_exchange_info()
        info = ExchangeInfo.from_json(info_json)
        return [BinanceAsset(name=symbol.symbol) for symbol in info.symbols]

    async def get_klines(
            self,
            symbol: str,
            start_date: str,
            end_date: str,
            interval: str,
            limit: int
    ) -> [HistoricalKLine]:
        klines = await self._async_client.get_historical_klines(
            symbol=symbol,
            start_str=start_date,
            end_str=end_date,
            interval=interval,
            limit=limit
        )

        klines_objects = [HistoricalKLine(json.dumps(kline)) for kline in klines]

        return klines_objects

    async def subscribe(self, tickers: [str]) -> AsyncGenerator[BinanceKLine, None]:
        streams = [f"{ticker.lower()}@kline_1m" for ticker in tickers]
        try:
            async with self._socket_manager.multiplex_socket(streams) as ts:
                while True:
                    print(f"Socket receive start: {tickers}", ts)
                    res = await asyncio.wait_for(ts.recv(), timeout=60.0)
                    kline = BinanceKLine(res)
                    await self.send_unsubscribe_command(ts)
                    print(f'Receive symbol: {kline.symbol}, open price: {kline.open_price}')
                    yield kline

        except asyncio.CancelledError:
            print(f"Cancelled {tickers}")
        except asyncio.TimeoutError:
            print(f"Timeout exceeded while waiting for data from the socket. {tickers}")
        finally:
            print(f"Finally {tickers}")
            await self._async_client.close_connection()

    async def send_unsubscribe_command(self, ws):
        unsubscribe_message = {
            "method": "UNSUBSCRIBE",
            "params": ["ethusdt@kline_1m"],
            "id": 1  # The ID can be any unique identifier
        }
        await asyncio.wait_for(ws.ws.send(json.dumps(unsubscribe_message)), timeout=10)
