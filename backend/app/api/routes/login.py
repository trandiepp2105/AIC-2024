from fastapi import FastAPI, HTTPException, APIRouter

from pydantic import BaseModel
import requests
import json
import os


router = APIRouter()

FILE_PATH = "./session_data.json"

class LoginInfo(BaseModel):
    username: str
    password: str

# Hàm để lưu dữ liệu vào file JSON
def save_to_file(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file)

# Hàm để đọc dữ liệu từ file JSON
def load_from_file():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    return {}

# Route để đăng nhập và lưu sessionID và evaluationID
@router.post("/")
def login(login_info: LoginInfo):
    login_data = {"username": login_info.username, "password": login_info.password}

    try:
        response = requests.post("https://eventretrieval.one/api/v2/login", json=login_data)
        response.raise_for_status()

        data = response.json()
        session_id = data.get("sessionId")

        if session_id:
            # Lấy evaluationID sau khi có sessionID
            eval_response = requests.get(
                "https://eventretrieval.one/api/v2/client/evaluation/list",
                params={"session": session_id}
            )
            eval_response.raise_for_status()

            eval_data = eval_response.json()
            print("eval_data: ", eval_data)
            evaluation_id = eval_data[0].get("id")

            # Lưu sessionID và evaluationID vào file, ghi đè lên dữ liệu cũ
            session_data = {
                "sessionID": session_id,
                "evaluationID": evaluation_id
            }
            save_to_file(session_data)
            return {"sessionID": session_id, "evaluationID": evaluation_id}
        else:
            raise HTTPException(status_code=500, detail="Session ID not found in response data")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route để lấy thông tin sessionID và evaluationID
@router.get("/")
def get_login_info():
    print("get login info")
    session_data = load_from_file()

    if session_data.get("sessionID") and session_data.get("evaluationID"):
        return {
            "sessionID": session_data["sessionID"],
            "evaluationID": session_data["evaluationID"],
        }
    else:
        raise HTTPException(status_code=404, detail="Session ID or Evaluation ID not found")
