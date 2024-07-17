from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select
from models import Frame, FrameBase
from api.deps import SessionDep
from pydantic import BaseModel

import crud
router = APIRouter()

class FrameIDs(BaseModel):
    frame_ids: List[int]

@router.get("/{frame_id}")
def get_frame(session: SessionDep, frame_id: Optional[int] = None) -> Any:
    """
    Retrieve frames by frame_id.
    """
    if frame_id is None:
        raise HTTPException(status_code=400, detail="frame_id is required")
    frame = crud.get_frame(session, frame_id)
    if frame is None:
        raise HTTPException(status_code=404, detail="Frame not found")
    return frame

@router.get("/")
def get_frame(session: SessionDep, frame_id: Optional[int] = None) -> Any:
    """
    Retrieve frames by frame_id.
    """
    if frame_id is None:
        frame = crud.get_all_frames(session)
        return frame
    
    frame = crud.get_frame(session, frame_id)
    return frame

@router.post(
    "/query",
)
def get_frames(session: SessionDep, frame_ids: FrameIDs) -> Any:
    """
    Retrieve frames by a list of frame_ids.
    """
    frames = crud.get_frames(session, frame_ids.frame_ids)
    return frames


@router.post(
    "/",
)
def create_frame(session: SessionDep, frame_data: FrameBase) -> Frame:
    """
    Create a frame.
    """
    frame = crud.create_frame(session, frame_data)
    return frame

