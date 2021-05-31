from fastapi import APIRouter

from api.api_v1.endpoints import subscribe

api_router = APIRouter()
api_router.include_router(subscribe.router, prefix="/user", tags=["Subscribe"])
