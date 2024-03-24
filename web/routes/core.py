from quart import Quart, render_template, request, stream_with_context, make_response, send_from_directory


class Route:
    app: Quart = None

    def __init__(self, app: Quart):
        self.app = app
        self.setup_routes()

    def setup_routes(self):
        pass
