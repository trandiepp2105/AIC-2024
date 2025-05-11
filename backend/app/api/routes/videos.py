from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, Request, Query
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from app.api.deps import SessionDep
from app.core.config import settings
from app import crud
import os

router = APIRouter()
# @router.get("/")
# def get_videos(
#     request: Request,
#     session: SessionDep,
#     limit: int = Query(10, ge=1, le=100),  # Số lượng kết quả trên mỗi trang
#     offset: int = Query(0, ge=0)  # Vị trí bắt đầu
# ) -> Any:
#     """
#     Retrieve all videos with pagination support.
#     """
#     videos = crud.read_videos(session, limit=limit, offset=offset)
#     total_videos = crud.count_videos(session)

#     if not videos:
#         raise HTTPException(status_code=404, detail="No videos found")

#     next_offset = offset + limit
#     prev_offset = offset - limit

#     next_url = (
#         f"{request.url.path}?limit={limit}&offset={next_offset}"
#         if next_offset < total_videos else None
#     )
#     previous_url = (
#         f"{request.url.path}?limit={limit}&offset={prev_offset}"
#         if prev_offset >= 0 else None
#     )

#     return {
#         "count": total_videos,
#         "next": next_url,
#         "previous": previous_url,
#         "results": videos
#     }

@router.get("/")
def get_video_by_video_name(session: SessionDep, video_name: Optional[str] = None) -> Any:
    """
    Retrieve video by video_name.
    """
    if video_name is None:
        raise HTTPException(status_code=400, detail="video_name is required")
    
    video = crud.get_video(session, video_name=video_name)
    
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    return video

@router.get("/{video_id}")
def get_video(session: SessionDep, video_id: Optional[int] = None) -> Any:
    """
    Retrieve video by video_id.
    """
    if video_id is None:
        raise HTTPException(status_code=400, detail="video_id is required")
    video = crud.get_video(session, video_id=video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    return video
    # return Response(content=video, headers=headers)
