from app.models.company import ControlColumns
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class CompanyBase(BaseModel):
    key: str
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

    class Config:
        orm_mode = True