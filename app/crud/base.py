from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from psycopg2.errors import UniqueViolation
from app.db.base_class import Base
from app import models
from fastapi import Depends, HTTPException, status
from app.api import dependencies as deps
from sqlalchemy.exc import IntegrityError, IntegrityError

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(
        self,
        db: Session,
        *,
        obj_in: CreateSchemaType,
        created_by: int
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        if created_by:
            # setattr(db_obj, "created_by", db_obj.created_by)
            db_obj.created_by = created_by
            db_obj.created_at = datetime.now()
        db.add(db_obj)
        # db.commit()
        db.flush() # db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        modified_by: int
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj) # Todos los datos a guardar
        if isinstance(obj_in, dict):
            update_data = obj_in # Si se paso un dato nuevo se agrega aca
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data: # Revisar todas las columnas
            if field in update_data: # Si alguna column se encuentra en el dato que quiero modificar
                setattr(db_obj, field, update_data[field]) # Se actualiza el objeto a guardar con ese dato nuevo
        if modified_by:
            # setattr(db_obj, "modified_by", db_obj.modified_by)
            db_obj.modified_by = modified_by
            db_obj.modified_at = datetime.now()
        db.add(db_obj)
        # db.commit()
        # db.refresh(db_obj)
        db.flush()
        return db_obj

    def delete(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

# TODO - Atrapar excepciones de todo tipo. create()
# try:
#     obj_in_data = jsonable_encoder(obj_in)
#     db_obj = self.model(**obj_in_data)  # type: ignore
#     if created_by:
#         # setattr(db_obj, "created_by", db_obj.created_by)
#         db_obj.created_by = created_by
#         db_obj.created_at = datetime.now()
#     db.add(db_obj)
#     db.commit()
#     db.refresh(db_obj)
# except IntegrityError as e:
#     print('--------------------------------111111111111111111111')
#     if e.orig.pgcode == 23505:
#         pass
#     if e.orig.pgcode is not None:
#         print(e.orig.pgcode)
#         print(e.orig.pgerror)
#         #print(e.orig.pgdetail)
#         print('------------------------------')
#         print(dir(e.orig.pgcode))
#     print('---------------------------------22222222222222')
#     # 23000 	IntegrityConstraintViolation 	IntegrityError
#     # 23001 	RestrictViolation 	IntegrityError
#     # 23502 	NotNullViolation 	IntegrityError
#     # 23503 	ForeignKeyViolation 	IntegrityError
#     # 23505 	UniqueViolation 	IntegrityError
#     # 23514 	CheckViolation 	IntegrityError
#     # 23P01 	ExclusionViolation 	IntegrityError
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="Could not validate cr1edent1ials",
#     )
#     # if ex.orig.pgcode == '23502':
#     #     print("Data could not be uploaded to sql_table: " + ex.orig.diag.message_primary)
#     # else:
#     #     raise