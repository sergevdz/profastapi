from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ControlColumns(BaseModel):
    id: int
    created_by: int
    created_at: datetime
    modified_by: Optional[int]
    modified_at: Optional[datetime]