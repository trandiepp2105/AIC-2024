from typing import Any, List, Optional, Tuple
from fastapi import APIRouter,Request, Query, HTTPException, status, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from app.api.deps import SessionDep
from app import crud
import sys
import os
import logging
import random
import time
# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# # Import tuyệt đối
from ai.search_index import search_index
from ai.search_index import search_tem
from elastic_search.elastic.elasticsearch_schema import CaptionSearch, VietOCRSearch, ParseqSearch

caption_search = CaptionSearch(hosts=['http://elasticsearch:9200'])
caption_search.setup()

vietocr_search = VietOCRSearch(hosts=['http://elasticsearch:9200'])
vietocr_search.setup()

parseq_search = ParseqSearch(hosts=['http://elasticsearch:9200'])
parseq_search.setup()
# OCRSearch.setup(hosts=['http://elasticsearch:9200'])
# CaptionSearch.setup(hosts=['http://elasticsearch:9200'])
router = APIRouter()

class BaseFrameQueryModel(BaseModel):
    priority: int
    value: Optional[str] = None

class RawTextQueryModel(BaseModel):
    priority: int
    value: Optional[List[str]] = []
class ObjectModel(BaseModel):
    class_name: str = Field(None, alias='className')
    quantity: Optional[int]
    class Config:
        populate_by_name = True

class ObjectsModel(BaseModel):
    priority: int
    value: Optional[List[ObjectModel]] = None


class ColorTableModel(BaseModel):
    column: int
    row: int
    table: List[List[str]]

class ColorsModel(BaseModel):
    priority: int
    value: ColorTableModel

class SearchRequest(BaseModel):
    raw_text: RawTextQueryModel = Field(alias='rawText')
    next_frame_query: BaseFrameQueryModel = Field(alias='nextFrameText')
    objects: ObjectsModel
    time: BaseFrameQueryModel
    colors: ColorsModel
    image: BaseFrameQueryModel
    speech: BaseFrameQueryModel
    ocr: BaseFrameQueryModel
    class Config:
        populate_by_name = True

import random
from typing import List, Tuple

def generate_random_frame_query(num_queries: int = 500) -> List[Tuple[str, int]]:
    video_names = [f"L01_V{str(i).zfill(3)}" for i in range(1, 30)]
    max_frames = 25 * 20 * 60  # FPS * minutes per video * seconds per minute
    max_frames = max_frames // 7
    frame_queries = []
    for _ in range(num_queries):
        video_name = random.choice(video_names)
        # Chọn ngẫu nhiên một số chia hết cho 7 giữa 1 và max_frames
        frame_number = random.randint(1, max_frames) * 7
        frame_queries.append((video_name, frame_number))

    return frame_queries


@router.post("/array")
def text_search_array(
    search_request: SearchRequest,
    session: SessionDep,
):
    try:
        frames = []
        ocr_value = search_request.ocr.value
        speech_value = search_request.speech.value
        # start_time = time.time()
        # temp_search = OCRSearch.search_ocr(query=ocr_value, top_k=3500)
        # end_time = time.time() 
        if ocr_value:
            # frames = OCRSearch.search_ocr(query=ocr_value, top_k=300)
            # frames = vietocr_search.search_field(query=ocr_value, top_k=100)
            frames = parseq_search.search_field(query=ocr_value, top_k=100)
            pass
        elif speech_value: 
            # print("caption hosts: ", caption_search.hosts)
            frames = caption_search.search_field(query=speech_value, top_k=200)
            
        else:
            # frames = generate_random_frame_query(100)
            #model_dump
            search_info = search_request.model_dump()
            frames = search_index(search_info, 100)
        # frames = crud.get_mul_frames(session=session, frames_query=frames_query)
        frames_data = [{"video_name": video_name, "frame_number": frame_number} for video_name, frame_number in frames]


        result = {
            "message": "Search text successfully",
            "result": frames_data
        }

        # elapsed_time = end_time - start_time  # tính thời gian chạy
        # print(f"Thời gian search: {elapsed_time} giây")
        # if frames_query:

        #     logger.info(f"result: {frames_query}")

        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except HTTPException as e:
        # Bắt lỗi HTTPException và trả về thông báo lỗi
        logger.error(f"HTTPException occurred: {e.detail}")
        raise e

    except Exception as e:
        # Bắt tất cả các lỗi khác và ghi log
        logger.error(f"An error occurred during search: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.post("/grid")
def text_search_grid(
    search_request: SearchRequest,
    session: SessionDep,
):
    try:
        #model_dump
        search_info = search_request.model_dump()
        ocr_value = search_request.ocr.value
        speech_value = search_request.speech.value
        frames = search_tem(search_info, 100)


        frames_data = [
            [{"video_name": video_name, "frame_number": frame_number} for video_name, frame_number in sublist]
            for sublist in frames
        ]
        result = {
            "message": "Search text successfully",
            "result": frames_data
        }

        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except HTTPException as e:
        # Bắt lỗi HTTPException và trả về thông báo lỗi
        logger.error(f"HTTPException occurred: {e.detail}")
        raise e

    except Exception as e:
        # Bắt tất cả các lỗi khác và ghi log
        logger.error(f"An error occurred during search: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")



