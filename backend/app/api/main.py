from fastapi import APIRouter

# from routes import frames, search
# from app.api.routes import frames, search
from app.api.routes import frames, search, classes, videos, submit, team_picked_frame, login

api_router = APIRouter()
api_router.include_router(frames.router, prefix="/frames", tags=["frames"])
api_router.include_router(videos.router, prefix="/videos", tags=["videos"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(classes.router, prefix="/classes", tags=["classes"])
api_router.include_router(submit.router, prefix="/submit", tags=["submit"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(team_picked_frame.router, prefix="/team-picked-frame", tags=["team_picked_frame"])