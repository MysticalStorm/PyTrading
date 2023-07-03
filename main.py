from quart import Quart
from trading.binance.core import Binance
from trading.trading_manager import TradingManager
from web.core import WebCore
from web.database.core import Database

def main(app):
    binance1 = Binance()
    database = Database(app)
    manager = TradingManager(binance1, database)
    web = WebCore(app, database, manager)
    web.run()

if __name__ == "__main__":
    app = Quart(__name__, template_folder="web/templates/")
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
    main(app)
    print("Finish")