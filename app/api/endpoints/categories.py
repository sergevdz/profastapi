from fastapi.params import Body
from sqlalchemy.sql.sqltypes import Boolean
from app.models import category
from app.models.category import Category
from app.models.movement import Movement
from app.crud import warehouse
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app.schemas.movement import MovementCreate, MovementResponse, MovementUpdate
from sqlalchemy.orm import Session
from app.api import dependencies as deps
from app import crud
from app import models
from datetime import datetime

router = APIRouter()


@router.get("/")
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve categories.
    """
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories


@router.post("/")
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    code: str = Body(...),
    name: str = Body(...),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Create new movement.
    """
    category = Category()
    category.created_at = datetime.now()
    category.created_by = current_user.id
    category.code = code
    category.name = name
    db.add(category)
    db.commit()
    
    db.refresh(category)

    return category


def has_new_data(model: Movement, movement_update: MovementUpdate) -> Boolean:
    if (model.type_id != movement_update.type_id or model.warehouse_id != movement_update.warehouse_id):
        return True
    return False

@router.put("/{id}")
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    code: str = Body(...),
    name: str = Body(...),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a category.
    """
    # Validar que exista la categoría
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="The category does not exist.",
        )
    # Guardar datos
    category.modified_at = datetime.now()
    category.modified_by = current_user.id
    category.code = code
    category.name = name
    db.add(category)
    
    db.commit()

    db.refresh(category)
    return category

@router.delete("/{id}")
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int
) -> Any:
    """
    Delete a category.
    """
    # Validar que exista la categoría
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="The category does not exist.",
        )
    db.delete(category)
    db.commit()
    return category
