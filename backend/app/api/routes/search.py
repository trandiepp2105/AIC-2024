from typing import Any, List, Optional
from fastapi import APIRouter,Request, Query, HTTPException
from models import Frame, FrameBase
from pydantic import BaseModel, Field
from api.deps import SessionDep
import crud
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
    frame_ids = [1,3,5,7,9, 10, 11,12, 13, 15, 17, 19]
    frames = crud.get_mul_frames(session, frame_ids)
    return frames

# @router.post("/image")
# def image_search()