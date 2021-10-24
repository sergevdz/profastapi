from app.crud.base import CRUDBase
from app.models import Movement
from app.schemas.movement import MovementCreate, MovementUpdate
from sqlalchemy.orm import Session
from typing import Optional

class CRUDItem(CRUDBase[Movement, MovementCreate, MovementUpdate]):
    def get_unique(self, db: Session, *, type_id: int, warehouse_id: int, inc: int) -> Optional[Movement]:
        return db.query(Movement).filter(
            Movement.type_id == type_id,
            Movement.warehouse_id == warehouse_id,
            Movement.inc == inc,
        ).first()


    def get_count(self, db: Session, *, type_id: int, warehouse_id: int) -> int:
        count = db.query(Movement).filter(
            Movement.type_id == type_id,
            Movement.warehouse_id == warehouse_id,
        ).count()
        return count


movement = CRUDItem(Movement)
