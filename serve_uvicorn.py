from quart import Quart
from web.core import WebCore

def create_app():
    app = Quart(__name__, template_folder="web/templates/", static_folder="web/static/")
    web = WebCore(app)
    web.run_uvicorn()

if __name__ == "__main__":
    create_app()