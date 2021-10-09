from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.warehouse import WarehouseCreate, WarehouseResponse, WarehouseUpdate
from sqlalchemy.orm import Session
from app.api import dependencies as deps
from app import crud
from app import models

router = APIRouter()


def validate_data_or_raise(db: Session, warehouse_create: WarehouseCreate):
    company = crud.company.get(db, id=warehouse_create.company_id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="The company does not exist.",
        )

    warehouse = crud.warehouse.get_by_key(db, key=warehouse_create.key)
    if warehouse:
        raise HTTPException(
            status_code=400,
            detail="The warehouse with this key already exists.",
        )

    warehouse = crud.warehouse.get_by_name(db, name=warehouse_create.name)
    if warehouse:
        raise HTTPException(
            status_code=400,
            detail="The warehouse with this name already exists.",
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
    validate_data_or_raise(db, warehouse_create)

    warehouse = crud.warehouse.create(
        db,
        obj_in=warehouse_create,
        created_by=current_user.id
    )
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

    validate_data_or_raise(db, warehouse_update)

    warehouse = crud.warehouse.update(
        db,
        db_obj=warehouse,
        obj_in=warehouse_update,
        modified_by=current_user.id
    )
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
    return warehouse
