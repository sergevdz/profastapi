from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from app.db.base_class import Base
from .control_columns import ControlColumns


if TYPE_CHECKING:
    from .warehouse import Warehouse  # noqa: F401
    pass


class Company(Base, ControlColumns):
    __tablename__ = "companies"
    code = Column(String(5), unique=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)

    # child_warehouses = relationship("Warehouse", back_populates="parent_company")
    warehouses = relationship("Warehouse", back_populates="company")