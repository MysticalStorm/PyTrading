from sqlalchemy import Column, String, Integer
from ..core import Model


class Generic(Model):
    content = String()
