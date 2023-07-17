from private.credentials import *
from binance.client import AsyncClient
from binance.streams import BinanceSocketManager
from ..interface import Platform
from .asset import BinanceAsset
from .balance import BinanceBalance
import json
import asyncio
from .models.kline import BinanceKLine


class Binance(Platform):
    _klines = []

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
        return [BinanceAsset(name=symbol_info['symbol']) for symbol_info in tickers]

    @property
    async def tokens(self) -> [BinanceAsset]:
        info = await self._async_client.get_exchange_info()
        result = set([])
        for symbol_info in info["symbols"]:
            result.add(symbol_info["baseAsset"])
            result.add(symbol_info["quoteAsset"])
        return [BinanceAsset(name=token) for token in result]

    @property
    async def klines(self) -> [BinanceKLine]:
        return self._klines

    async def subscribe(self, ticker: str):
        try:
            async with self._socket_manager.kline_socket(ticker) as ts:
                while 1:
                    print(f"Socket receive start: {ticker}", ts)
                    res = await asyncio.wait_for(ts.recv(), timeout=60.0)
                    kline = BinanceKLine(res)
                    self._klines.append(kline)
                    print(f'Receive symbol: {kline.symbol}, open price: {kline.open_price}')
        except asyncio.CancelledError:
            print(f"Cancelled {ticker}")
        except asyncio.TimeoutError:
            print(f"Timeout exceeded while waiting for data from the socket. {ticker}")
        finally:
            print(f"Finally {ticker}")
            # await self._async_client.close_connection()
