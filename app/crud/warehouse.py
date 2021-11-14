from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
# from app.models.item import Item
from app.models import Warehouse
# from app.schemas.item import ItemCreate, ItemUpdate
from app.schemas.warehouse import WarehouseCreate, WarehouseUpdate


class CRUDItem(CRUDBase[Warehouse, WarehouseCreate, WarehouseUpdate]):  
    # TODO - Crear funcion template para buscar obj por cualquier columna
    def get_by_code(self, db: Session, *, code: str) -> Optional[Warehouse]:
        return db.query(Warehouse).filter(Warehouse.code == code).first()

    def get_by_name(self, db: Session, *, name: str) -> Optional[Warehouse]:
        return db.query(Warehouse).filter(Warehouse.name == name).first()

    def get_by_company(self, db: Session, *, company_id: int) -> Optional[List[Warehouse]]:
        return db.query(Warehouse).filter(Warehouse.company_id == company_id) # .first()

    pass


warehouse = CRUDItem(Warehouse)
