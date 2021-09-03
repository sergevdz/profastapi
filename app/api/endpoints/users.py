from typing import Any, List

from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse
from sqlalchemy.orm import Session
from app.api import dependencies as deps
from app import crud
# from app import models

router = APIRouter()


# @router.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]


# @router.get("/users/me", tags=["users"])
# async def read_user_me():
#     return {"username": "fakecurrentuser"}


# @router.get("/users/{username}", tags=["users"])
# async def read_user(username: str):
#     return {"username": username}

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