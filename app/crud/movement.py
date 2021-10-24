from fastapi.exceptions import HTTPException
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


    def get_new_increment(self, db: Session, *, type_id: int, warehouse_id: int) -> int:
        data = db.query(Movement.inc).filter(
            Movement.type_id == type_id,
            Movement.warehouse_id == warehouse_id
        ).order_by(Movement.inc.desc()).first()
        if data.inc is None:
            raise HTTPException(
                status_code=400,
                detail="Can't generete new Folio with provided data.",
            )
        return data.inc + 1


movement = CRUDItem(Movement)
