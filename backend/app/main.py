from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


# from api.main import api_router
from app.api.main import api_router
from app.core.config import settings
import os

app = FastAPI()
video_directory = settings.VIDEOS_VOLUME_DIR
frames_directory = settings.FRAMES_VOLUME_DIR
# Kiểm tra nếu thư mục tồn tại và mount các thư mục tĩnh
if os.path.isdir(video_directory):
    app.mount("/videos", StaticFiles(directory=video_directory), name="videos")
else:
    raise Exception(f"Directory {video_directory} does not exist")

if os.path.isdir(frames_directory):
    app.mount("/frames", StaticFiles(directory=frames_directory), name="frames")
else:
    raise Exception(f"Directory {frames_directory} does not exist")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, DELETE, PUT"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Root page change part 2"}

@app.get("/infor")
async def infor():
    return {
        "SQLALCHEMY_DATABASE_URI": settings.SQLALCHEMY_DATABASE_URI,
    }


