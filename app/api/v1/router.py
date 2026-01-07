from fastapi import APIRouter
from api.v1.routes.users import router as users_router
from api.v1.routes.ai_gen import router as ai_gen_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(ai_gen_router, prefix="/ai", tags=["ai"])