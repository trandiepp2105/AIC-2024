from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import aiofiles
import logging

# from api.main import api_router
from app.api.main import api_router
from app.core.config import settings
import os
from elastic_search.elastic.load_captions_into_elastic import load_data_into_elastic as load_captions_into_elastic
from elastic_search.elastic.load_parseq_into_elastic import load_data_into_elastic as load_parseq_into_elastic
from elastic_search.elastic.load_vietocr_into_elastic import load_data_into_elastic as load_vietocr_into_elastic
flag_file = '.elastic_flag'

# Kiểm tra nếu file cờ đã tồn tại
if os.path.exists(flag_file):
    print("Data has already been loaded into Elasticsearch. Skipping...")
else:
    # Nếu chưa có file cờ, gọi các hàm load và tạo file cờ
    load_captions_into_elastic()
    load_parseq_into_elastic()
    load_vietocr_into_elastic()
    
    # Tạo file cờ sau khi load xong
    with open(flag_file, 'w') as f:
        f.write('All data loaded into Elasticsearch.')
    print("All data loaded and flag file created.")

app = FastAPI()
video_directory = settings.VIDEOS_VOLUME_DIR


app.add_middleware(
    CORSMiddleware,
    # allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origins=["*"],
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

# if os.path.isdir(frames_directory):
#     app.mount("/stream/frames", StaticFiles(directory=frames_directory), name="stream_frames")
# else:
#     raise Exception(f"Directory {frames_directory} does not exist")

# @app.get("/stream/videos/{video_name}")
# async def stream_video(video_name: str, request: Request):
#     file_path = os.path.join(video_directory, video_name)
#     if not os.path.isfile(file_path):
#         raise HTTPException(status_code=404, detail="Video not found")

#     file_stat = os.stat(file_path)
#     file_size = file_stat.st_size

#     async def iter_file(file_path: str, start: int = 0, end: int = None):
#         async with aiofiles.open(file_path, "rb") as file:
#             await file.seek(start)
#             chunk_size = 1024 * 1024
#             while True:
#                 if end and start + chunk_size > end:
#                     chunk_size = end - start
#                 data = await file.read(chunk_size)
#                 if not data:
#                     break
#                 start += len(data)
#                 yield data

#     range_header = request.headers.get("range")
#     if range_header:
#         range_start, range_end = range_header.replace("bytes=", "").split("-")
#         range_start = int(range_start) if range_start else 0
#         range_end = int(range_end) if range_end else file_size - 1
#         range_end = min(range_end, file_size - 1)
#         content_length = (range_end - range_start) + 1

#         logging.debug(f"Range: {range_start}-{range_end}, Content-Length: {content_length}")

#         response_headers = {
#             "Content-Range": f"bytes {range_start}-{range_end}/{file_size}",
#             "Accept-Ranges": "bytes",
#             "Content-Length": str(content_length),
#             "Content-Type": "video/mp4",
#         }
#         return StreamingResponse(
#             iter_file(file_path, start=range_start, end=range_end + 1),
#             status_code=206,
#             headers=response_headers,
#             media_type="video/mp4",
#         )

#     return StreamingResponse(
#         iter_file(file_path),
#         headers={
#             "Content-Length": str(file_size),
#             "Content-Type": "video/mp4",
#             "Accept-Ranges": "bytes",
#         },
#         media_type="video/mp4",
#     )
