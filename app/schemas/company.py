from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class CompanyBase(BaseModel):
    key: str
    name: str


# Properties to receive via API on creation
class CompanyCreate(CompanyBase):
    pass


# Properties to receive via API on update
class CompanyUpdate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    id: int

    class Config:
        orm_mode = True