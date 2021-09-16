from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    # from .item import Item  # noqa: F401
    pass


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(5), unique=True, index=True, nullable=False)
    name = Column(String(100), unique=True, index=True, nullable=False)