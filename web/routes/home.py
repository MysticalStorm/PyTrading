from .core import Route
from quart import Quart, render_template, request, stream_with_context, make_response, send_from_directory
import hashlib
import os
from trading.adapter import TradingManager
from database.core import Database

class HomeRoute(Route):

    def __init__(self, app: Quart, manager: TradingManager, db: Database):
        super().__init__(app)
        self.manager = manager
        self.db = db

    @staticmethod
    def calculate_file_hash(file_path):
        with open(file_path, 'rb') as file:
            content = file.read()
            hash_object = hashlib.md5(content)
            return hash_object.hexdigest()
    def setup_routes(self):
        @self.app.route('/search')
        async def search():
            query = request.args.get('q', default="", type=str)
            query = query.lower()

            tickers = await self.manager.tickers()
            matched_tickers = [ticker.name for ticker in tickers if query in ticker.name.lower()]

            return {"data": matched_tickers}

        @self.app.route('/', methods=['GET'])
        async def home():
            message = await self.db.get_all_messages()
            if message:
                message = message[0].content

            # Calculate the hash of the CSS file
            css_path = os.path.join(self.app.static_folder, 'css', 'main.css')
            css_hash = self.calculate_file_hash(css_path)

            # Calculate the hash of the JS file
            js_path = os.path.join(self.app.static_folder, 'js', 'main.js')
            js_hash = self.calculate_file_hash(js_path)

            return await render_template('home.html', message=message, css_hash=css_hash, js_hash=js_hash)

        @self.app.route('/details', methods=['GET'])
        async def details():
            # Calculate the hash of the CSS file
            css_path = os.path.join(self.app.static_folder, 'css', 'main.css')
            css_hash = self.calculate_file_hash(css_path)

            # Calculate the hash of the JS file
            js_path = os.path.join(self.app.static_folder, 'js', 'details.js')
            js_hash = self.calculate_file_hash(js_path)

            return await render_template('details.html', css_hash=css_hash, js_hash=js_hash)

        # Route to serve JavaScript files
        @self.app.route('/static/js/<path:filename>')
        async def serve_js(filename):
            return await send_from_directory('web/static/js', filename, mimetype='application/javascript')