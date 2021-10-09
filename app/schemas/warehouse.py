from app.models.company import ControlColumns
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from .control_columns import ControlColumns


class WarehouseBase(BaseModel):
    key: str
    name: str
    company_id: int


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseUpdate(WarehouseBase):
    pass


class WarehouseResponse(ControlColumns, WarehouseBase):
    # id: int
    # created_by: int
    # created_at: datetime
    # modified_by: Optional[int]
    # modified_at: Optional[datetime]

    class Config:
        orm_mode = True