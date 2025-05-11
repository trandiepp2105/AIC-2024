from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import json
import requests
from app import crud
from app.api.deps import SessionDep

router = APIRouter()

UPLOAD_DIR = "./submit_logs"


FILE_PATH = "./session_data.json"
def load_from_file():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    return {}

class Answer(BaseModel):
    query_mode: str
    video_name: str
    frame_number: int
    answer: str

def calculate_time_from_frame(frame_number: int, fps: int) -> int:
    return round((frame_number / fps) * 1000)  # Convert to milliseconds

@router.post("/")
async def submit(session: SessionDep, answer_data: Answer):
    session_data = load_from_file()
    evaluation_id = session_data.get("evaluationID")
    session_id = session_data.get("sessionID")

    if not evaluation_id or not session_id:
        raise HTTPException(status_code=400, detail="Evaluation ID or Session ID not found in session data.")

    video = crud.get_video(session, video_name=answer_data.video_name)
    fps = video.fps

    # Calculate time from frame number and fps
    time = calculate_time_from_frame(answer_data.frame_number, fps)

    # Determine body based on query mode
    if answer_data.query_mode == "QA":
        body = {
            "answerSets": [
                {
                    "answers": [
                        {
                            "text": f"{answer_data.answer}-{answer_data.video_name}-{time}",
                        },
                    ],
                },
            ],
        }
    elif answer_data.query_mode == "TEXT":
        body = {
            "answerSets": [
                {
                    "answers": [
                        {
                            "mediaItemName": answer_data.video_name,
                            "start": time,
                            "end": time,
                        },
                    ],
                },
            ],
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid queryMode provided. Expected 'QA' or 'TEXT'.")

    # Send request to external API
    try:
        submit_endpoint = f"https://eventretrieval.one/api/v2/submit/{evaluation_id}"
        response = requests.post(submit_endpoint, json=body, params={"session": session_id})
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the response from the external API
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.post()
# # Hàm kiểm tra nếu file đã tồn tại
# def get_unique_file_name(file_name, file_extension):
#     # Tạo đường dẫn cho file
#     file_location = os.path.join(UPLOAD_DIR, f"{file_name}{file_extension}")
    
#     # Nếu file chưa tồn tại thì trả về luôn tên đó
#     if not os.path.exists(file_location):
#         return file_location

#     # Nếu file tồn tại, bắt đầu thêm index từ 1
#     index = 1
#     while True:
#         new_file_name = f"{file_name}_{index}{file_extension}"
#         file_location = os.path.join(UPLOAD_DIR, new_file_name)
#         if not os.path.exists(file_location):
#             return file_location
#         index += 1

# # Endpoint để upload file
# @router.post("/")
# async def submit(file: UploadFile = File(...)):
#     print("submit frames!")
#     try:
#         if not os.path.exists(UPLOAD_DIR):
#             os.makedirs(UPLOAD_DIR)

#         # Lấy tên gốc của file
#         original_file_name = file.filename
#         file_name, file_extension = os.path.splitext(original_file_name)

#         # Gọi hàm để lấy tên file duy nhất
#         unique_file_location = get_unique_file_name(file_name, file_extension)

#         # Lưu file
#         with open(unique_file_location, "wb") as f:
#             content = await file.read()
#             f.write(content)

#         # Lấy tên file vừa được lưu để trả về
#         saved_file_name = os.path.basename(unique_file_location)

#         return JSONResponse(content={"message": "File uploaded successfully", "file_name": saved_file_name}, status_code=200)

#     except Exception as e:
#         print("error: ", e)
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
