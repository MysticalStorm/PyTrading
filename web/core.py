import asyncio

from quart import Quart, render_template, request, stream_with_context, make_response, send_from_directory
from database.core import Database
import json
import uvicorn
import hypercorn
from hypercorn.asyncio import serve

from trading.binance.core import Binance
from trading.adapter import TradingManager
from trading.models.kline import KLine
from typing import Optional
import hashlib
import os


def calculate_file_hash(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        hash_object = hashlib.md5(content)
        return hash_object.hexdigest()


class WebCore:
    manager: TradingManager = None

    def __init__(self, app: Quart):
        self.app = app
        self.db = Database(app)

        @app.before_serving
        async def startup():
            binance1 = Binance()
            self.manager = TradingManager(binance1, self.db)

        @self.app.route('/search')
        async def search():
            query = request.args.get('q', default="", type=str)
            query = query.lower()

            tickers = await self.manager.tickers()
            matched_tickers = [ticker.name for ticker in tickers if query in ticker.name.lower()]

            return {"data": matched_tickers}

        @self.app.route('/subscribe', methods=['POST'])
        async def subscribe():
            data = await request.json
            currency = data.get('symbol')
            print("Subscribe on: ", currency)
            if currency:
                # create a new instance of Binance and call the subscribe method
                await self.manager.subscribe(currency)  # Pass the currency value to the subscribe method

                return {"message": "Subscription successful"}
            else:
                return {"error": "Invalid request"}

        @self.app.route('/unsubscribe', methods=['POST'])
        async def unsubscribe():
            data = await request.json
            currency = data.get('symbol')
            print("Subscribe on: ", currency)
            if currency:
                # create a new instance of Binance and call the subscribe method
                await self.manager.unsubscribe(currency)  # Pass the currency value to the subscribe method

                return {"message": "Subscription successful"}
            else:
                return {"error": "Invalid request"}

        @self.app.route('/', methods=['GET'])
        async def home():
            message = await self.db.get_all_messages()
            if message:
                message = message[0].content

            # Calculate the hash of the CSS file
            css_path = os.path.join(app.static_folder, 'css', 'main.css')
            css_hash = calculate_file_hash(css_path)

            # Calculate the hash of the JS file
            js_path = os.path.join(app.static_folder, 'js', 'main.js')
            js_hash = calculate_file_hash(js_path)

            return await render_template('home.html', message=message, css_hash=css_hash, js_hash=js_hash)

        @app.route('/stream')
        async def stream():
            @stream_with_context
            async def event_stream():
                while True:
                    # Here you would usually pull updates from your application.
                    # Instead, we're going to generate a random number every second.
                    kline: Optional[KLine] = None
                    klines = await self.manager.klines()
                    if klines:
                        data = {kline.symbol: {"open": kline.open_price} for kline in klines}
                        # Convert the list of dictionaries to JSON format
                        json_data = json.dumps(data)
                        yield 'data: {}\n\n'.format(json_data)
                    await asyncio.sleep(1)

            response = await make_response(event_stream(), {'Content-Type': 'text/event-stream'})
            response.timeout = None  # No timeout for this route
            return response

        # Route to serve JavaScript files
        @app.route('/static/js/<path:filename>')
        async def serve_js(filename):
            return await send_from_directory('web/static/js', filename, mimetype='application/javascript')

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