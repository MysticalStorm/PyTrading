from quart import Quart
from web.core import WebCore

app = Quart(__name__, template_folder="web/templates/", static_folder="web/static/")


def main(app):
    web = WebCore(app)
    web.run()


if __name__ == "__main__":
    main(app)
