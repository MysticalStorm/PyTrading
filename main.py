from quart import Quart
from web.core import WebCore

app = Quart(__name__, template_folder="web/templates/", static_folder="web/static/")
WebCore(app)