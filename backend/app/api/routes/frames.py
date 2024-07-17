from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Query
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
def get_frames(
    request: Request,
    session: SessionDep,
    limit: int = Query(10, ge=1, le=100),  # Số lượng kết quả trên mỗi trang
    offset: int = Query(0, ge=0)  # Vị trí bắt đầu
) -> Any:
    """
    Retrieve all frames with pagination support.
    """
<<<<<<< HEAD
    if frame_id is None:
        frame = crud.get_all_frames(session)
        return frame
    
    frame = crud.get_frame(session, frame_id)
    return frame
=======
    frames = crud.read_frames(session, limit=limit, offset=offset)
    total_frames = crud.count_frames(session)

    if not frames:
        raise HTTPException(status_code=404, detail="No frames found")

    next_offset = offset + limit
    prev_offset = offset - limit

    next_url = (
        f"{request.url.path}?limit={limit}&offset={next_offset}"
        if next_offset < total_frames else None
    )
    previous_url = (
        f"{request.url.path}?limit={limit}&offset={prev_offset}"
        if prev_offset >= 0 else None
    )

    return {
        "count": total_frames,
        "next": next_url,
        "previous": previous_url,
        "results": frames
    }
>>>>>>> ababde4ca2cbf3431cf7a0e53303da36340d105d

@router.post(
    "/query",
)
def get_frames(session: SessionDep, frame_ids: FrameIDs) -> Any:
    """
    Retrieve frames by a list of frame_ids.
    """
    frames = crud.get_mul_frames(session, frame_ids.frame_ids)
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

