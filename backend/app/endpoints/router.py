from fastapi import APIRouter

from endpoints.api.user import router as user_router
from endpoints.api.admin import router as admin_router


api_router = APIRouter()

# Include all version routers
api_router.include_router(user_router, prefix="/user")
api_router.include_router(admin_router, prefix="/admin")