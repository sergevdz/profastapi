from app.models.company import ControlColumns
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.schemas.warehouse import WarehouseResponse

class CompanyBase(BaseModel):
    code: str
    name: str


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    id: int
    created_by: int
    created_at: datetime
    modified_by: Optional[int]
    modified_at: Optional[datetime]

    # warehouses: List[WarehouseResponse] = [] # Scheme, not model

    class Config:
        orm_mode = True