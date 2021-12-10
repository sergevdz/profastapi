from sqlalchemy import Column, String
from app.db.base_class import Base
from .control_columns import ControlColumns


class Category(Base, ControlColumns):
    __tablename__ = "categories"
    code = Column(String(5), unique=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)