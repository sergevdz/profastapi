from sqlalchemy import Column, Integer, ForeignKey
from app.db.base_class import Base
from .control_columns import ControlColumns


class Movement(Base, ControlColumns):
    __tablename__ = "movements"
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    type_id = Column(Integer, ForeignKey("movement_types.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    inc  = Column(Integer, nullable=False)
    status  = Column(Integer, nullable=False)

    # company = relationship("Company", back_populates="warehouses")
