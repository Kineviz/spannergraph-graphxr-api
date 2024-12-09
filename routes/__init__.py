from fastapi import APIRouter
from .spanner import router as spanner_router

api_router = APIRouter()
api_router.include_router(spanner_router, prefix="/spanner", tags=["spanner"])