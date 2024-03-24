import asyncio

from quart import Quart, render_template, request, stream_with_context, make_response, send_from_directory
from database.core import Database

import uvicorn
import hypercorn
from hypercorn.asyncio import serve

from trading.binance.core import Binance
from trading.adapter import TradingManager
from trading.models.kline import KLine
from typing import Optional

from web.routes.stream import StreamRoute
from web.routes.home import HomeRoute

class WebCore:
    manager: TradingManager = None

    def __init__(self, app: Quart):
        self.app = app
        self.db = Database(app)

        @app.before_serving
        async def startup():
            binance1 = Binance()
            self.manager = TradingManager(binance1, self.db)
            self.home_route = HomeRoute(app, self.manager, db=self.db)
            self.stream_route = StreamRoute(app, self.manager)

    def run_hypercorn(self):
        from hypercorn.config import Config
        from .logs.core import Logger
        self.app.asgi_app = Logger(self.app.asgi_app)
        config = Config()
        config.bind = ["localhost:5000"]
        asyncio.run(serve(self.app, config))

    def run_uvicorn(self):
        # , reload_includes=["*.html", "*.js", "*.css"]
        uvicorn.run("main:app", host="127.0.0.1", port=5002, loop="asyncio", reload=True)