from fastapi import FastAPI
from fastapi.routing import APIRoute
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from api.main import api_router
from core.database import init_db, load_data_from_folders
from contextlib import asynccontextmanager
from core.config import settings
import logging

app = FastAPI()

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

@app.get("/infor")
async def infor():
    return {
        "SQLALCHEMY_DATABASE_URI": settings.SQLALCHEMY_DATABASE_URI,
    }

# FRAME_DIR = "D:\\AIC-2024-DATA\\frames"
# VIDEO_DIR = "D:\\AIC-2024-DATA\\videos"

# def main():
#     init_db()
#     # load_data_from_folders(frames_folder=FRAME_DIR, videos_folder=VIDEO_DIR)

#     # Chạy ứng dụng FastAPI
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# # if __name__ == "__main__":
# #     main()
# main()