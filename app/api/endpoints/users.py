from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from sqlalchemy.orm import Session
from app.api import dependencies as deps
from app import crud
# from app import models


router = APIRouter(
    # prefix="/users",
    # tags=["users"],
    dependencies=[Depends(deps.get_current_active_superuser)]
    # responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[UserResponse])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
    # current_user: models.User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_all(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserResponse)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_create: UserCreate
    # current_user: models.User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_create.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists.",
        )
    user = crud.user.create(db, obj_in=user_create)
    # Revisar si puedo enviar email
    # if settings.EMAILS_ENABLED and user_in.email:
    #     send_new_account_email(
    #         email_to=user_in.email, username=user_in.email, password=user_in.password
    #     )
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_update: UserUpdate
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist.",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_update)
    return user

@router.delete("/{user_id}", response_model=UserResponse)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist.",
        )
    # Super user can't be deleted!
    if user.is_superuser:
        # TODO - If logged user is SuperAdmin, send message "Super user can't be deleted!"
        raise HTTPException(
            status_code=404,
            detail="The user doesn't have enough privileges",
        )
    user = crud.user.delete(db, id=user_id)
    return user
