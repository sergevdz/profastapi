from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from app.schemas.user import UserResponse, UserCreate
from sqlalchemy.orm import Session
from app.api import dependencies as deps
from app import crud
from passlib.context import CryptContext
from app import models

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -----------------------------------
# TODO - get_current_active_superuser
# current_user: models.User = Depends(deps.get_current_active_superuser),
# Si no eres Super Usuario, no puedes ver los usuarios
# -------------------------------------
@router.get("/", response_model=List[UserResponse])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserResponse) # Como se conecta schema con models?
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate
    # current_user: models.User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    # Revisar si puedo enviar email
    # if settings.EMAILS_ENABLED and user_in.email:
    #     send_new_account_email(
    #         email_to=user_in.email, username=user_in.email, password=user_in.password
    #     )
    db.rollback()
    return user


# @router.get("/fake")
# def read_users(
#     skip: int = 0,
#     limit: int = 100
# ) -> Any:
#     """
#     Retrieve fake users.
#     """
#     pwd = '12345'
#     hasshed_pwd = pwd_context.hash(pwd)
#     valid_pwd = pwd_context.verify(pwd, hasshed_pwd)

#     myobj = pwd, hasshed_pwd, valid_pwd

#     users = [
#         myobj
#     ]
#     return users