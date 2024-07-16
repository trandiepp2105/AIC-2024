from fastapi import APIRouter

# from app.api.routes import frames
from api.routes import frames

api_router = APIRouter()
api_router.include_router(frames.router, prefix="/frames", tags=["frames"])
