from sqlalchemy.sql.sqltypes import Boolean
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

router = APIRouter()

def validate_data_or_raise(db: Session, movement_create: MovementCreate):
    movement = crud.movement.get_unique(
        db,
        type_id=movement_create.type_id,
        warehouse_id=movement_create.warehouse_id, 
        inc=movement_create.inc
    )
    # This exception should never be runned
    if movement:
        raise HTTPException(
            status_code=400,
            detail="There is already a movement with that folio.",
        )


@router.get("/", response_model=List[MovementResponse])
def read_movements(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve movements.
    """
    movements = crud.movement.get_all(db, skip=skip, limit=limit)
    return movements


@router.post("/", response_model=MovementResponse)
def create_movement(
    *,
    db: Session = Depends(deps.get_db),
    movement_create: MovementCreate,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Create new movement.
    """
    # Create transaction
    transaction = crud.transaction.create(db, created_by=current_user.id)
    movement_create.transaction_id = transaction.id

    # Set incrementable
    new_inc = crud.movement.get_new_increment(
        db,
        type_id=movement_create.type_id,
        warehouse_id=movement_create.warehouse_id
    )
    movement_create.inc = new_inc

    validate_data_or_raise(db, movement_create)

    movement = crud.movement.create(
        db,
        obj_in=movement_create,
        created_by=current_user.id
    )

    db.commit()

    return movement

# @router.get("/count/{type_id}/{warehouse_id}")
# def create_movement_count(
#     *,
#     db: Session = Depends(deps.get_db),
#     type_id: int,
#     warehouse_id: int
# ) -> Any:
#     """
#     Create new movement.
#     """
#     count = crud.movement.get_count(
#         db,
#         type_id=type_id,
#         warehouse_id=warehouse_id
#     )
#     print(count)

#     return count


def has_new_data(model: Movement, movement_update: MovementUpdate) -> Boolean:
    if (model.type_id != movement_update.type_id or model.warehouse_id != movement_update.warehouse_id):
        return True
    return False

@router.put("/{id}", response_model=MovementResponse)
def update_movement(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    movement_update: MovementUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a movement.
    """

    movement = crud.movement.get(db, id=id)
    if not movement:
        raise HTTPException(
            status_code=404,
            detail="The movement does not exist.",
        )
    
    if (not has_new_data(movement, movement_update)):
        return movement

    new_inc = crud.movement.get_new_increment(
        db,
        type_id=movement_update.type_id,
        warehouse_id=movement_update.warehouse_id
    )
    movement_update.inc = new_inc

    validate_data_or_raise(db, movement_update)

    movement = crud.movement.update(
        db,
        db_obj=movement,
        obj_in=movement_update,
        modified_by=current_user.id
    )
    
    db.commit()
    return movement


@router.delete("/{id}", response_model=MovementResponse)
def delete_movement(
    *,
    db: Session = Depends(deps.get_db),
    id: int
) -> Any:
    """
    Delete a movement.
    """
    movement = crud.movement.get(db, id=id)
    if not movement:
        raise HTTPException(
            status_code=404,
            detail="The movement does not exist.",
        )
    
    movement = crud.movement.delete(db, id=id)
    return movement
