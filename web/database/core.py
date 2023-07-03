from quart_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column

db = SQLAlchemy()

class Database:
    def __init__(self, app):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        self.app = app
        db.init_app(app)
        app.before_serving(self.before_serving)

    async def before_serving(self):
        async with self.app.app_context():
            db.create_all()

    async def save(self, message):
        new_message = Message(content=message)
        db.session.add(new_message)
        db.session.commit()

    async def get_all_messages(self):
        async with self.app.app_context():
            users = db.session.execute(db.select(Message))
            return users.scalars().all()


class Message(db.Model):
    id = Column(Integer, primary_key=True)
    content = Column(String(500))
