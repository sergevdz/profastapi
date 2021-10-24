from app.models.company import ControlColumns
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from .control_columns import ControlColumns


class TransactionBase(BaseModel):
    pass


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionResponse(ControlColumns, TransactionBase):
    # id: int
    # created_by: int
    # created_at: datetime
    # modified_by: Optional[int]
    # modified_at: Optional[datetime]

    class Config:
        orm_mode = True