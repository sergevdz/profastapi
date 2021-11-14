from app.models.company import ControlColumns
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from .control_columns import ControlColumns


class WarehouseBase(BaseModel):
    code: str
    name: str


class WarehouseCreate(WarehouseBase):
    company_id: int


class WarehouseUpdate(WarehouseBase):
    pass


class WarehouseResponse(WarehouseBase, ControlColumns):
    # id: int
    # created_by: int
    # created_at: datetime
    # modified_by: Optional[int]
    # modified_at: Optional[datetime]

    class Config:
        orm_mode = True