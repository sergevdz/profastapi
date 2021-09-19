from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue

from app.db.base_class import Base

if TYPE_CHECKING:
    # from .item import Item  # noqa: F401
    pass

class ControlColumns():
    id = Column(Integer, primary_key=True)
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=FetchedValue())
    modified_by = Column(DateTime, nullable=True)
    modified_at = Column(Integer, server_default=FetchedValue())

class Company(Base, ControlColumns):
    __tablename__ = "companies"
    # id = Column(Integer, primary_key=True)
    # created_by = Column(Integer, nullable=False)
    # created_at = Column(DateTime, nullable=False)
    # modified_by = Column(DateTime, nullable=False)
    # modified_at = Column(Integer, nullable=False)
    
    key = Column(String(5), unique=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)