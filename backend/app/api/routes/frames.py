from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlmodel import col, delete, func, select
from app.api.deps import SessionDep
from pydantic import BaseModel

from app import crud
router = APIRouter()

@router.get("/adjacent")
def get_adjacent_frames(video_name: str, frame_number: int, duration: int, fps: int = 25):
    try:
        frames = crud.get_adjacent_frames_by_range(video_name, frame_number, duration, fps)
        if not frames:
            raise HTTPException(status_code=404, detail="No frames found")
        return {"frames": frames}
    except Exception as e:
        print("err: ", e)
        raise HTTPException(status_code=500, detail=str(e))

# @router.get("/")
# def get_frames(
#     request: Request,
#     session: SessionDep,
#     video_name: Optional[str] = None,
#     frame_number: Optional[int] = None,
#     limit: int = Query(10, ge=1, le=100),  # Số lượng kết quả trên mỗi trang
#     offset: int = Query(0, ge=0)  # Vị trí bắt đầu
# ) -> Any:
#     """
#     Retrieve frames. If query params video_name and frame_number or frame_id are provided,
#     retrieve a specific frame. Otherwise, retrieve all frames with pagination.
#     """
#     # Check if specific frame retrieval is requested
#     if video_name is not None and frame_number is not None:
#         frame_query = None
#         if video_name is not None and frame_number is not None:
#             frame_query = (video_name, frame_number)

#         try:
#             frame = crud.get_frame(session=session, frame_query=frame_query, frame_id=frame_id)
#             if not frame:
#                 raise HTTPException(status_code=404, detail="Frame not found")
#             return frame
#         except HTTPException as e:
#             raise HTTPException(status_code=e.status_code, detail=e.detail)

#     # Otherwise, retrieve all frames with pagination
#     frames = crud.read_frames(session, limit=limit, offset=offset)
#     total_frames = crud.count_frames(session)

#     if not frames:
#         raise HTTPException(status_code=404, detail="No frames found")

#     next_offset = offset + limit
#     prev_offset = offset - limit

#     next_url = (
#         f"{request.url.path}?limit={limit}&offset={next_offset}"
#         if next_offset < total_frames else None
#     )
#     previous_url = (
#         f"{request.url.path}?limit={limit}&offset={prev_offset}"
#         if prev_offset >= 0 else None
#     )

#     return {
#         "count": total_frames,
#         "next": next_url,
#         "previous": previous_url,
#         "results": frames
#     }
