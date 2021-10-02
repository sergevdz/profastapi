from app.models.company import ControlColumns
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class WarehouseBase(BaseModel):
    key: str
    name: str
    company_id: int

class WarehouseCreate(WarehouseBase):
    pass


class WarehouseUpdate(WarehouseBase):
    pass


class WarehouseResponse(WarehouseBase):
    id: int
    created_by: int
    created_at: datetime
    modified_by: Optional[int]
    modified_at: Optional[datetime]

    class Config:
        orm_mode = True