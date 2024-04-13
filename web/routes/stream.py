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
        @self.app.route('/subscriptions', methods=['GET'])
        async def subscriptions():
            arrray_of_tickers = self.manager.subscriptions()
            data = {"tickers": arrray_of_tickers}
            # Convert the list of dictionaries to JSON format
            json_data = json.dumps(data)
            return json_data

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

        @self.app.route('/stream', methods=['GET'])
        async def stream():
            query = request.args.get('q', default="", type=str)
            ticker = query.lower()

            @stream_with_context
            async def event_stream():
                try:
                    async for kline in await self.manager.subscribe(ticker):
                        if kline:
                            data = {kline.symbol: {"open": kline.open_price}}
                            json_data = json.dumps(data)
                            yield 'data: {}\n\n'.format(json_data)
                        await asyncio.sleep(1)
                except Exception as e:
                    # Log the exception which might indicate a disconnect or another issue
                    print("Stream error:", str(e))
                    await self.manager.unsubscribe(ticker)

            response = await make_response(event_stream(), {'Content-Type': 'text/event-stream'})
            response.timeout = None  # No timeout for this route
            return response
