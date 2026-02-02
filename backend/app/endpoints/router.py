from fastapi import APIRouter

from app.endpoints.api.user import router as user_router
from app.endpoints.api.admin import router as admin_router
from app.endpoints.api.ingest_data import router as data_router
from app.endpoints.api.ask_bot import router as bot_router

api_router = APIRouter()

# Include all version routers
api_router.include_router(user_router, prefix="/user")
api_router.include_router(data_router, prefix='/data')
api_router.include_router(bot_router, prefix='/bot')
api_router.include_router(admin_router, prefix="/admin")