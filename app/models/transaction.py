from app.db.base_class import Base
from .control_columns import ControlColumns


class Transaction(Base, ControlColumns):
    __tablename__ = "transactions"

    pass