from app.models.warehouse import Warehouse
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.warehouse import WarehouseCreate, WarehouseResponse, WarehouseUpdate
from sqlalchemy.orm import Session
from app.api import dependencies as deps
from app import crud
from app import models

router = APIRouter()


def validate_duplicate_code(db: Session, *, code: str, exclude_id: int = None):
    warehouse = crud.warehouse.get_by_code(db, code=code)
    if exclude_id:
        warehouse = db.query(Warehouse).filter(Warehouse.id != exclude_id, Warehouse.code == code).first()
    if warehouse:
        raise HTTPException(
            status_code=400,
            detail="The is already a warehouse with this code.",
        )


def validate_duplicate_name(db: Session, name: str, exclude_id: int = None):
    warehouse = crud.warehouse.get_by_name(db, name=name)
    if exclude_id:
        warehouse = db.query(Warehouse).filter(Warehouse.id != exclude_id, Warehouse.name == name).first()
    if warehouse:
        raise HTTPException(
            status_code=400,
            detail="The is already a warehouse with this name.",
        )

def validate_if_warehouse_exists(db: Session, id: int):
    warehouse = crud.warehouse.get(db, id=id)
    if not warehouse:
        raise HTTPException(
            status_code=404,
            detail="The warehouse does not exist.",
        )


@router.get("/", response_model=List[WarehouseResponse])
def read_warehouses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve warehouses.
    """
    warehouses = crud.warehouse.get_all(db, skip=skip, limit=limit)
    return warehouses


@router.post("/", response_model=WarehouseResponse)
def create_warehouse(
    *,
    db: Session = Depends(deps.get_db),
    warehouse_create: WarehouseCreate,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Create new warehouse.
    """
    warehouse_create.company_id = 1 # Always 1
    validate_duplicate_code(db, warehouse_create.code)
    validate_duplicate_name(db, warehouse_create.name)

    warehouse = crud.warehouse.create(
        db,
        obj_in=warehouse_create,
        created_by=current_user.id
    )

    db.commit()
    return warehouse

@router.put("/{id}", response_model=WarehouseResponse)
def update_warehouse(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    warehouse_update: WarehouseUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a warehouses.
    """
    warehouse = crud.warehouse.get(db, id=id)
    if not warehouse:
        raise HTTPException(
            status_code=404,
            detail="The warehouse does not exist.",
        )

    validate_if_warehouse_exists(db, warehouse.id)
    validate_duplicate_code(db, exclude_id=warehouse.id, code=warehouse_update.code)
    validate_duplicate_name(db, exclude_id=warehouse.id, name=warehouse_update.name)

    warehouse = crud.warehouse.update(
        db,
        db_obj=warehouse,
        obj_in=warehouse_update,
        modified_by=current_user.id
    )
    db.commit()
    return warehouse


@router.delete("/{id}", response_model=WarehouseResponse)
def delete_warehouse(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    # current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Delete a warehouse.
    """
    warehouse = crud.warehouse.get(db, id=id)
    if not warehouse:
        raise HTTPException(
            status_code=404,
            detail="The warehouse does not exist.",
        )
    
    warehouse = crud.warehouse.delete(db, id=id)
    db.commit()
    return warehouse
