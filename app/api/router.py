from fastapi import APIRouter

# from app.api.endpoints import items, login, users, utils
from app.api.endpoints import login, users, companies # , utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
