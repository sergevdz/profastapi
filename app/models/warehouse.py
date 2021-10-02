from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue

from app.db.base_class import Base
from .control_columns import ControlColumns


if TYPE_CHECKING:
    # from .item import Item  # noqa: F401
    pass


class Warehouse(Base, ControlColumns):
    __tablename__ = "companies"
    key = Column(String(5), unique=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
    
    # parent_company = relationship("Company", back_populates="child_warehouses")
    company = relationship("Company", back_populates="warehouses")
