from private.credentials import *
from binance.client import AsyncClient
from binance.streams import BinanceSocketManager
from ..interface import Platform
from .asset import BinanceAsset
from .balance import BinanceBalance
import json
import asyncio


class Binance(Platform):
    active_sockets = []

    def __init__(self):
        self._balance = None

        self._async_client = AsyncClient(api_key, secret_key, testnet=True)
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
    async def all_tickers(self) -> [str]:
        info = await self._async_client.get_exchange_info()
        print(info)

        info2 = await self._async_client.get_all_tickers()
        print(info2)

        return [symbol_info['symbol'] for symbol_info in info['symbols']]

    async def connect(self):
        try:
            async with self._socket_manager.kline_socket("ethusdt") as ts:
                print("Socket created", ts)
                res = await asyncio.wait_for(ts.recv(), timeout=5.0)  # timeout set to 5 seconds
                print(f'recv {res}')

            print("Through socket creation")
        except asyncio.TimeoutError:
            print("Timeout exceeded while waiting for data from the socket.")
        finally:
            await self._async_client.close_connection()