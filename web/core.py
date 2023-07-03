from quart import Quart, render_template, request
from trading.trading_manager import TradingManager
from .database.core import Database
import json

class WebCore:
    def __init__(self, app: Quart, db: Database, manager: TradingManager):
        self.app = app
        self.manager = manager
        self.db = db
        @self.app.route('/', methods=['GET', 'POST'])
        async def home():
            message = await self.db.get_all_messages()
            message = message[0].content
            if request.method == 'POST':
                form = await request.form
                if form.get('action') == 'Subscribe':
                    # create a new instance of Binance and call the subscribe method
                    await self.manager.subscribe()  # replace with the appropriate call for your Binance class
            return await render_template('home.html', message=message)

    def run(self):
        self.app.run(debug=True)
