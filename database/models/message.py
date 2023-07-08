from sqlalchemy import Column, String, Integer
from ..core import Model


class Message(Model):
    id = Column(Integer, primary_key=True)
    content = Column(String(500))
