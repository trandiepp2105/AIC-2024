from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.routing import APIRoute
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from api.main import api_router
from core.database import load_data_from_folders
from contextlib import asynccontextmanager
from core.config import settings
import os

import logging

app = FastAPI()
video_directory = "D:/AIC-2024-DATA/videos"
frames_directory = "D:/AIC-2024-DATA/frames"

# Kiểm tra nếu thư mục tồn tại và mount các thư mục tĩnh
if os.path.isdir(video_directory):
    app.mount("/videos", StaticFiles(directory=video_directory), name="videos")
else:
    raise Exception(f"Directory {video_directory} does not exist")

if os.path.isdir(frames_directory):
    app.mount("/frames", StaticFiles(directory=frames_directory), name="frames")
else:
    raise Exception(f"Directory {frames_directory} does not exist")
# Cấu hình CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    # Thêm các domain khác nếu cần
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Root page"}

@app.get("/infor")
async def infor():
    return {
        "SQLALCHEMY_DATABASE_URI": settings.SQLALCHEMY_DATABASE_URI,
    }

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, DELETE, PUT"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response
