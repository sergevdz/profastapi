from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from app.db.base_class import Base
from .control_columns import ControlColumns


class MovementType(Base, ControlColumns):
    __tablename__ = "movement_types"
    key = Column(String(5), unique=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)