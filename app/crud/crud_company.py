from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
# from app.models.item import Item
from app.models import Company
# from app.schemas.item import ItemCreate, ItemUpdate
from app.schemas.company import CompanyCreate, CompanyUpdate


class CRUDItem(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    # def create_with_owner(
    #     self, db: Session, *, obj_in: CompanyCreate, owner_id: int
    # ) -> Company:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data, owner_id=owner_id)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def get_multi_by_owner(
    #     self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    # ) -> List[Company]:
    #     return (
    #         db.query(self.model)
    #         .filter(Company.owner_id == owner_id)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )
    pass


company = CRUDItem(Company)
