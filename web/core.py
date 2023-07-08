import asyncio

from quart import Quart, render_template, request, stream_with_context, make_response
from trading.trading_manager import TradingManager
from database.core import Database
import time
import uvicorn

# https://pgjones.gitlab.io/quart/how_to_guides/sync_code.html

class WebCore:
    def __init__(self, app: Quart, db: Database, manager: TradingManager):
        self.app = app
        self.manager = manager
        self.db = db
        print("Webcore ok")
        @self.app.route('/', methods=['GET', 'POST'])
        async def home():
            print("Home")

            message = await self.db.get_all_messages()
            if message:
                message = message[0].content
            if request.method == 'POST':
                form = await request.form
                if form.get('action') == 'Subscribe':
                    # create a new instance of Binance and call the subscribe method
                    await self.manager.subscribe()  # replace with the appropriate call for your Binance class
            return await render_template('home.html', message=message)

        @app.route('/stream')
        async def stream():
            @stream_with_context
            async def event_stream():
                while True:
                    # Here you would usually pull updates from your application.
                    # Instead, we're going to generate a random number every second.
                    yield 'data: {}\n\n'.format(time.asctime())
                    await asyncio.sleep(1)

            response = await make_response(event_stream(), {'Content-Type': 'text/event-stream'})
            response.timeout = None  # No timeout for this route
            return response

    def run(self):
        uvicorn.run(self.app, host="127.0.0.1", port=5000)
