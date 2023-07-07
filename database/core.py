import asyncio

from quart_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column
from quart_sqlalchemy.extension import Table, MetaData
import config.db as config
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declared_attr
from quart_sqlalchemy.extension import declarative_base
from functools import reduce
import os

class _DBModel(object):
    def save(self):
        db.session.merge(self)
        db.session.commit()

    @declared_attr
    def __tablename__(cls):
        return "T" + cls.__name__

    @property
    def primary_key(self):
        t = Table(type(self).__tablename__, MetaData(), autoload=True, autoload_with=db.engine)
        primary_keys = reduce(lambda x, y: {**x, **{y.name: getattr(self, y.name)}}, t.primary_key.columns.values(), {})
        return primary_keys

    def is_equal(self, other):
        return self.__class__ == other.__class__ and self.primary_key == other.primary_key

    def __eq__(self, other):
        return type(self) is type(other) and self.is_equal(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def create_table(cls):
        if hasattr(cls, "__table__"):
            db.create_table(cls.__table__)


Model = declarative_base(cls=_DBModel)
db = SQLAlchemy(model_class=Model)


class Database:
    def __init__(self, app):
        self.db = db
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join('..', config.database_path)}"
        self.app = app
        self.db.init_app(app)
        app.before_serving(self.before_serving)

    async def before_serving(self):
        async with self.app.app_context():
            self.db.create_all()

    async def save(self, message):
        new_message = Message(content=message)
        self.db.session.add(new_message)
        self.db.session.commit()

    def create_all_meta(self):
        Model.metadata.create_all(self.db.engine)

    async def create_table(self, table: Table):
        def ctable():
            table.drop(self.db.engine)
            table.create(self.db.engine)

        return await asyncio.get_running_loop().run_in_executor(
            None, ctable
        )

    async def get_all_messages(self):
        async with self.app.app_context():
            users = self.db.session.execute(self.db.select(Message))
            return users.scalars().all()


class Message(Model):
    __tablename__ = "Messages"

    id = Column(Integer, primary_key=True)
    content = Column(String(500))
