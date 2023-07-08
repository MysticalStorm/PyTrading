import asyncio

from quart_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column
from sqlalchemy.inspection import inspect
from quart_sqlalchemy.extension import Table, MetaData
import config.db as config
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declared_attr
from quart_sqlalchemy.extension import declarative_base
from functools import reduce
import os
import concurrent.futures


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
    async def create_table(cls, database):
        if hasattr(cls, "__table__"):
            await database.async_create_table(cls.__table__)


Model = declarative_base(cls=_DBModel)
db = SQLAlchemy(model_class=Model)

from .models.message import Message


class Database:
    def __init__(self, app):
        self.db = db
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join('..', config.database_path)}"
        self.app = app
        self.db.init_app(app)
        app.before_serving(self.before_serving)

    async def before_serving(self):
        async with self.app.app_context():
            await Message.create_table(self)

    async def save(self, message):
        async def async_save():
            async with self.app.app_context():
                new_message = Message(content=message)
                new_message.save()

        return await asyncio.create_task(async_save())

    def create_all_meta(self):
        Model.metadata.create_all(self.db.engine)

    async def async_create_table(self, table: Table):
        async def create_table():
            async with self.app.app_context():
                if inspect(self.db.engine).has_table(table.name):
                    table.drop(self.db.engine)
                table.create(self.db.engine)

        return await asyncio.create_task(create_table())

    async def get_all_messages(self):
        async def messages():
            async with self.app.app_context():
                users = self.db.session.execute(self.db.select(Message))
                return users.scalars().all()

        return await asyncio.create_task(messages())
