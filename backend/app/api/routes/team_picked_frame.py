from typing import List, Optional, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlmodel import Session, select
from app.models import TeamPickedFrame
from app.api.deps import SessionDep
from pydantic import BaseModel
import logging
from app import crud
from app.core.database import engine
from threading import Lock
from enum import Enum
from collections import defaultdict

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
priority_lock = Lock()  
class MODE(str, Enum):
    TEXT = "TEXT"
    QA = "QA"
class TeamPickedFrameBase(BaseModel):
    video_name: str
    frame_number: int
    query_index: int
    mode: str
    # path: str
    answer: Optional[str]
    # duration: float
    class Config:
        from_attributes = True

def process_frame(frame_data: TeamPickedFrameBase):
    try:
        with Session(engine) as db_session:
            # Kiểm tra xem frame đã tồn tại chưa dựa trên video_name, frame_number, query_index và mode
            statement = select(TeamPickedFrame).where(
                TeamPickedFrame.video_name == frame_data.video_name,
                TeamPickedFrame.frame_number == frame_data.frame_number,
                TeamPickedFrame.query_index == frame_data.query_index,
                TeamPickedFrame.mode == frame_data.mode
            )
            existing_frame = db_session.exec(statement).first()

            if existing_frame:
                logger.info(f"Frame {frame_data.video_name}_{frame_data.frame_number} existing!")
                return None  # Nếu frame đã tồn tại, không thêm vào

            # Sử dụng khóa để đồng bộ hóa việc tính toán priority
            with priority_lock:
                # Tìm giá trị priority lớn nhất hiện tại
                max_priority_stmt = select(TeamPickedFrame.priority).order_by(TeamPickedFrame.priority.desc()).limit(1)
                max_priority = db_session.exec(max_priority_stmt).first()

                # Gán giá trị priority mới bằng max_priority + 1
                new_priority = (max_priority or 0) + 1

                # Tạo đối tượng mới với priority đã tính toán
                frame_obj = TeamPickedFrame(**frame_data.dict(), priority=new_priority)
                db_session.add(frame_obj)
                db_session.commit()
                db_session.refresh(frame_obj)
                return frame_obj
    except Exception as e:
        logger.error(f"Error processing frame: {e}")
        return None

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_team_picked(
    team_picked_frames: List[TeamPickedFrameBase],
    session: SessionDep  # Không cần dùng trong process_frame nữa nhưng cần để đảm bảo session đang hoạt động
):
    logger.info(f"Received team_picked_frames: {team_picked_frames}")
    added_frames = []
    
    try:
        # Xóa toàn bộ dữ liệu trong bảng trước khi thêm dữ liệu mới
        # session.query(TeamPickedFrame).delete()
        # session.commit()

        # Xử lý tuần tự từng frame
        for frame in team_picked_frames:
            result = process_frame(frame)
            if result:
                added_frames.append(result)
        print("team pick: ", team_picked_frames)
        return {"team_picked": added_frames}
    
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_team_picked_frames(
    session: SessionDep,
    query_index: Optional[int] = Query(None),
    mode: Optional[str] = Query(None),  # Thêm mode vào query parameter
):
    try:
        # Tạo truy vấn để lấy tất cả các frame
        statement = select(TeamPickedFrame)

        # Lọc theo query_index nếu được cung cấp
        if query_index is not None:
            statement = statement.where(TeamPickedFrame.query_index == query_index)

        # Lọc theo mode nếu được cung cấp
        if mode is not None:
            statement = statement.where(TeamPickedFrame.mode == mode)
        
        # Thực hiện truy vấn và sắp xếp các frame theo priority
        frames = session.exec(statement.order_by(TeamPickedFrame.priority)).all()

        if not frames:
            raise HTTPException(status_code=404, detail="No frames found")

        # Nếu không có query_index, nhóm frames theo query_index
        if query_index is None and mode is None:
            # Tạo một dictionary để nhóm các frames theo query_index
            grouped_frames = defaultdict(list)
            for frame in frames:
                grouped_frames[frame.query_index].append(frame)

            # Chuyển dictionary thành danh sách các danh sách frames và sắp xếp theo query_index
            grouped_frames_list = [group for _, group in sorted(grouped_frames.items())]
            return grouped_frames_list

        # Nếu có query_index, trả về danh sách frames bình thường
        return frames

    except Exception as e:
        logger.error(f"Error retrieving frames: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/", status_code=status.HTTP_200_OK)
def update_priority(
    frames_priority_update: List[TeamPickedFrameBase],
    session: SessionDep
):
    try:
        with priority_lock:
            for index, frame_data in enumerate(frames_priority_update):
                # Tìm frame trong bảng dựa trên video_name, frame_number, query_index và mode
                statement = select(TeamPickedFrame).where(
                    TeamPickedFrame.video_name == frame_data.video_name,
                    TeamPickedFrame.frame_number == frame_data.frame_number,
                    TeamPickedFrame.query_index == frame_data.query_index,
                    TeamPickedFrame.mode == frame_data.mode  # Thêm kiểm tra mode
                )
                existing_frame = session.exec(statement).first()

                if not existing_frame:
                    raise HTTPException(status_code=404, detail=f"Frame with video_name: {frame_data.video_name}, frame_number: {frame_data.frame_number}, query_index: {frame_data.query_index}, mode: {frame_data.mode} not found")

                # Cập nhật priority theo index trong mảng (index + 1)
                existing_frame.priority = index + 1
                session.add(existing_frame)

            session.commit()  # Commit toàn bộ các thay đổi

        return {"message": "Priority updated successfully"}
    except Exception as e:
        logger.error(f"Error updating priority: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update-answer/{id}", status_code=status.HTTP_200_OK)
def update_answer(
    session: SessionDep,
    id: int = Path(..., description="ID của frame cần cập nhật"),
    new_answer: str = Query(..., description="Giá trị mới của answer"),
):
    try:
        # Tìm frame trong bảng dựa trên id
        frame = session.get(TeamPickedFrame, id)

        if not frame:
            raise HTTPException(status_code=404, detail=f"Frame with id {id} not found")

        # Cập nhật answer mới
        frame.answer = new_answer
        session.add(frame)
        session.commit()  # Commit thay đổi
        session.refresh(frame)  # Tải lại frame sau khi commit

        return {"message": "Answer updated successfully", "updated_frame": frame}
    except Exception as e:
        logger.error(f"Error updating answer for frame id {id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating answer")


@router.delete("/{frame_id}", status_code=status.HTTP_200_OK)
def delete_team_picked_frame(
    frame_id: int,
    session: SessionDep
):
    try:
        # Tìm phần tử dựa trên id
        frame_to_delete = session.get(TeamPickedFrame, frame_id)

        if not frame_to_delete:
            raise HTTPException(status_code=404, detail="Frame not found")

        # Xóa phần tử
        session.delete(frame_to_delete)
        session.commit()

        # Cập nhật lại priority cho các phần tử còn lại
        with priority_lock:
            remaining_frames = session.exec(select(TeamPickedFrame).order_by(TeamPickedFrame.priority)).all()
            for index, frame in enumerate(remaining_frames):
                frame.priority = index + 1
                session.add(frame)
            session.commit()

        return {"message": "Frame deleted and priority updated successfully"}
    except Exception as e:
        logger.error(f"Error deleting frame: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-by-query-index/{query_index}", status_code=status.HTTP_200_OK)
def delete_team_picked_frame_by_query_index(
    session: SessionDep,
    query_index: int
    
):
    try:
        # Lấy tất cả các frame có query_index khớp
        frames_to_delete = session.exec(
            select(TeamPickedFrame).where(TeamPickedFrame.query_index == query_index)
        ).all()

        if not frames_to_delete:
            raise HTTPException(status_code=404, detail=f"No frames found with query_index {query_index}")

        # Xóa tất cả các frame
        for frame in frames_to_delete:
            session.delete(frame)

        session.commit()

        # Cập nhật lại priority cho các frame còn lại
        with priority_lock:
            remaining_frames = session.exec(select(TeamPickedFrame).order_by(TeamPickedFrame.priority)).all()
            for index, frame in enumerate(remaining_frames):
                frame.priority = index + 1
                session.add(frame)
            session.commit()

        return {"message": f"Frames with query_index {query_index} deleted and priority updated successfully"}

    except Exception as e:
        logger.error(f"Error deleting frames with query_index {query_index}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
