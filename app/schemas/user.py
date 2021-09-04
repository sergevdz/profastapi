from typing import List, Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    # hashed_password: str # Alwayds commented
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    hashed_password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    hashed_password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    #items: List[Item] = []
    pass

    class Config:
        orm_mode = True