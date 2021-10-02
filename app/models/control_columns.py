from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.schema import FetchedValue


class ControlColumns():
    id = Column(Integer, primary_key=True)
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=FetchedValue())
    modified_by = Column(DateTime, nullable=True)
    modified_at = Column(Integer, server_default=FetchedValue())
