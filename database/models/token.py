from sqlalchemy import Column, String, Integer
from ..core import Model


class Token(Model):
    id = Column(Integer, primary_key=True)
    content = Column(String(500))
