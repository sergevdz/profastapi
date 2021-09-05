from fastapi import FastAPI
from app.core.config import settings
from starlette.middleware.cors import CORSMiddleware

# from .dependencies import get_query_token, get_token_header
# from .internal import admin
# from .routers import items, users
from app.api.api import api_router

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(users.router)
# app.include_router(items.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )

# app.include_router(users.router)
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}