from .core import Route
from quart import Quart, render_template, request, stream_with_context, make_response, send_from_directory
from trading.adapter import TradingManager
import asyncio
import json


class StreamRoute(Route):

    def __init__(self, app: Quart, manager: TradingManager):
        super().__init__(app)
        self.manager = manager

    def setup_routes(self):
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

        @self.app.route('/stream')
        async def stream():
            @stream_with_context
            async def event_stream():
                while True:
                    klines = await self.manager.klines()
                    if klines:
                        kline = klines[-1]
                        if kline:
                            rsi = await self.manager.calculate_rsi_for_symbol(kline.symbol)
                            print(rsi)

                        data = {kline.symbol: {"open": kline.open_price} for kline in klines}
                        # Convert the list of dictionaries to JSON format
                        json_data = json.dumps(data)
                        yield 'data: {}\n\n'.format(json_data)
                    await asyncio.sleep(1)

            response = await make_response(event_stream(), {'Content-Type': 'text/event-stream'})
            response.timeout = None  # No timeout for this route
            return response
