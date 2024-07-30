from fastapi import APIRouter

# from routes import frames, search
# from app.api.routes import frames, search
from app.api.routes import frames, search, classes, videos

api_router = APIRouter()
api_router.include_router(frames.router, prefix="/frames", tags=["frames"])
api_router.include_router(videos.router, prefix="/videos", tags=["videos"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(classes.router, prefix="/classes", tags=["classes"])
