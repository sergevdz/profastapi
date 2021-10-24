from app.crud.base import CRUDBase
from app.models import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from sqlalchemy.orm import Session

class CRUDItem(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def create(
        self, db: Session, *, created_by: int
    ) -> Transaction:
        # obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(created_by=created_by)
        db.add(db_obj)
        # db.commit()
        db.flush() # db.refresh(db_obj)
        return db_obj


transaction = CRUDItem(Transaction)
