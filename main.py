from quart import Quart
from web.core import WebCore
from web.logs.core import Logger
import logging

app = Quart(__name__, template_folder="web/templates/", static_folder="web/static/")
WebCore(app)