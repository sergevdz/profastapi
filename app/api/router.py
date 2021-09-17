from fastapi import APIRouter

# from app.api.endpoints import items, login, users, utils
from app.api.endpoints import users, login # , utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
