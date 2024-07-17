from typing import Any, List, Optional
from fastapi import APIRouter,Request, Query, HTTPException
from pydantic import BaseModel, Field
from api.deps import SessionDep
import crud
import sys
import os
import logging
# Thêm thư mục gốc và thư mục ai vào sys.path
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
ai_path = os.path.join(base_path, 'ai')
scripts_path = os.path.join(ai_path, 'scripts')

sys.path.append(base_path)
sys.path.append(ai_path)
sys.path.append(scripts_path)

# Import tuyệt đối
from ai.search_index import search_text, image_search

router = APIRouter()


class SearchRequest(BaseModel):
    raw_text: Optional[str] = Field(None, alias='rawText')
    object: Optional[str] = None
    quantity: Optional[int] = None
    time: Optional[str] = None
    location: Optional[str] = None
    predicate: Optional[str] = None
    color: Optional[str] = None

    class Config:
        populate_by_name = True

@router.post("/text")
def text_search(
    search_request: SearchRequest,
    session: SessionDep,
):
    index, text_search_rel = search_text("a girl use a phone", 10)
    frame_ids = index[0]
    # frame_ids = [2,1,3,7,9, 10, 11,12, 13, 15, 17, 19]
    logging.warning(frame_ids)
    frames = crud.get_mul_frames(session, frame_ids)
    return frames

# @router.post("/image")
# def image_search()

