from app.models.company import ControlColumns
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .control_columns import ControlColumns


class MovementBase(BaseModel):
    # transaction_id: int
    type_id: int
    warehouse_id: int
    # inc: int
    status: int


class MovementCreate(MovementBase):
    transaction_id: Optional[int] = Field(-1, title="The description of the item")
    inc: Optional[int] = Field(-1, description="The price must be greater than zero")

# class MovementInternalCreate(MovementBase):
#     transaction_id: Optional[int]
#     inc: Optional[int]


class MovementUpdate(MovementBase):
    pass


class MovementResponse(MovementBase, ControlColumns):
    transaction_id: int
    inc: int

    class Config:
        orm_mode = True
