import asyncio
from trading.binance.core import Binance
from concurrent.futures import ThreadPoolExecutor

async def main():
    binance1 = Binance()
    binance2 = Binance()

    print(await binance1.all_tickers)

    with ThreadPoolExecutor(max_workers=2) as executor:
        await asyncio.gather(
            loop.run_in_executor(executor, asyncio.run, binance1.connect()),
            loop.run_in_executor(executor, asyncio.run, binance2.connect())
        )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("Finish")