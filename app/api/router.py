from fastapi import APIRouter, Depends

from app.api.endpoints import users, companies
from app.api import dependencies as deps

api_router = APIRouter(
    dependencies=[Depends(deps.get_current_active_user)]
)
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
