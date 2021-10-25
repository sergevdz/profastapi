from fastapi.encoders import jsonable_encoder
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

    def update(
        self, db: Session, *, db_obj: Movement, obj_in: MovementUpdate, modified_by: int
    ) -> Movement:
        obj_in_data = jsonable_encoder(obj_in)
    
        new_inc = self.get_new_increment(
            db,
            type_id=obj_in.type_id,
            warehouse_id=obj_in.warehouse_id
        )
        db_obj = self.model(**obj_in_data, modified_by=modified_by, inc=new_inc)
        db.add(db_obj)
        db.flush()
        return db_obj


movement = CRUDItem(Movement)
