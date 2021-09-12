from typing import List, Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: str # Optional[str] = None
    # hashed_password: str # Hidden for all users!
    is_active: Optional[bool] = True
    # is_superuser: Optional[bool] = False # Hidden for all users!


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    hashed_password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    #items: List[Item] = []
    pass

    class Config:
        orm_mode = True