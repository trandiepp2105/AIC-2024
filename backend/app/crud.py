from fastapi import Query, HTTPException
from typing import List, Tuple, Any
from sqlmodel import Session, select
from app.models import Video
import json
from app.core.config import redis_client

def get_video(session: Session, video_id: int = None, video_name: str = None) -> Any:
    if not video_id and not video_name:
        return None
    
    if video_id:
        key = f"video:{video_id}"
        
    elif video_name:
        video = session.query(Video).filter_by(video_name=video_name).first()
        if not video:
            return None
        video_id = video.id
        key = f"video:{video_id}"
    
    video_data = redis_client.get(key)
    if video_data:
        return Video(**json.loads(video_data))
    
    video = session.get(Video, video_id)
    if video:
        # Cache kết quả vào Redis
        redis_client.set(key, json.dumps(video.to_dict()))
    
    return video

def get_adjacent_frames_by_range(
    video_name: str, 
    frame_number: int, 
    duration: int, 
    fps: int = 25
) -> List[Tuple[str, int]]:
    # Tính số lượng frame cần lấy dựa trên thời lượng và fps cho mỗi phía
    frames_to_fetch = duration * fps

    # Điều chỉnh start_frame để nó là bội số của 7 và không nhỏ hơn 0
    start_frame = max(0, (frame_number - frames_to_fetch) // 7 * 7)
    end_frame = (frame_number + frames_to_fetch) // 7 * 7
    
    # Tạo mảng các số frame là bội số của 7 từ start_frame tới end_frame
    list_adjacent_frames = range(start_frame, end_frame + 1, 7)
    
    # Duyệt qua list_adjacent_frames và tạo list các tuple (video_name, frame_number)
    frames = [(video_name, frame_number) for frame_number in list_adjacent_frames]
    frames_data = [{"video_name": video_name, "frame_number": frame_number} for video_name, frame_number in frames]

    return frames_data

def get_mul_videos(session: Session, video_ids: List[int]) -> Any:
    results = []
    missing_video_ids = []

    # Check Redis cache first
    for video_id in video_ids:
        key = f"video:{video_id}"
        video_data = redis_client.get(key)
        if video_data:
            results.append(Video(**json.loads(video_data)))
        else:
            missing_video_ids.append(video_id)
    
    # Query the database for missing videos
    if missing_video_ids:
        videos = session.exec(select(Video).where(Video.id.in_(missing_video_ids))).all()
        for video in videos:
            # Cache the result in Redis
            key = f"video:{video.id}"
            redis_client.set(key, json.dumps(video.to_dict()))
            results.append(video)
    
    return results




# def count_frames(session: Session) -> int:
#     statement = select(func.count(Frame.id))
#     result = session.execute(statement).scalar_one()
#     return result

# def count_videos(session: Session) -> int:
#     statement = select(func.count(Video.id))
#     result = session.execute(statement).scalar_one()
#     return result

# def read_videos(
#     session: Session,
#     limit: int = Query(10, ge=1, le=10),
#     offset: int = Query(0, ge=0)
# ):
#     statement = select(Video).limit(limit).offset(offset)
#     results = session.exec(statement).all()
#     return results

# def read_frames(
#     session: Session,
#     limit: int = Query(10, ge=1, le=10),
#     offset: int = Query(0, ge=0)
# ):
#     statement = select(Frame).limit(limit).offset(offset)
#     results = session.exec(statement).all()
#     return results

# def get_frame(session: Session, frame_query: Tuple[str, int] = None, frame_id: int = None) -> Any:
#     # If an ID is provided, use it for the lookup
#     if frame_query is not None:
#         video_name, frame_number = frame_query
#         key = f"frame:{video_name}-{frame_number}"
#         frame_data = redis_client.get(key)
#         if frame_data:
#             return Frame(**json.loads(frame_data))
        
#         frame = session.exec(
#             select(Frame).where(Frame.frame_number == frame_number, Frame.path.contains(f"/{video_name}/"))
#         ).first()

#         if frame:
#             redis_client.set(key, json.dumps(frame.to_dict()))
#             return frame
#         else:
#             raise HTTPException(status_code=404, detail="Frame not found")

#     if frame_id is not None:
#         key = f"frame:{frame_id}"
#         frame_data = redis_client.get(key)
#         if frame_data:
#             return Frame(**json.loads(frame_data))
        
#         frame = session.get(Frame, frame_id)
#         if frame:
#             redis_client.set(key, json.dumps(frame.to_dict()))
#             return frame
#         else:
#             raise HTTPException(status_code=404, detail="Frame not found")

#     # If frame_query is provided, use it for the lookup

#     # If neither frame_id nor frame_query is provided, raise an error
#     raise HTTPException(status_code=400, detail="Either frame_id or frame_query must be provided")

# def get_mul_frames(session: Session, frames_query: List[Tuple[str, int]]) -> Any:
#     results_dict = {}
#     missing_video_frames = []

#     # Check Redis cache first
#     for video_name, frame_number in frames_query:
#         key = f"frame:{video_name}-{frame_number}"
#         frame_data = redis_client.get(key)
#         if frame_data:
#             results_dict[(video_name, frame_number)] = Frame(**json.loads(frame_data))
#         else:
#             missing_video_frames.append((video_name, frame_number))
    
#     # Query the database for missing frames
#     if missing_video_frames:
#         # for video_name, frame_number in missing_video_frames:
#         #     frame = session.exec(
#         #         select(Frame).where(Frame.frame_number == frame_number, Frame.path.contains(f"/{video_name}/"))
#         #     ).first()
#         #     if frame:
#         #         key = f"frame:{video_name}-{frame.frame_number}"
#         #         redis_client.set(key, json.dumps(frame.to_dict()))
#         #         results_dict[(video_name, frame_number)] = frame

#         frames_number = [frame_number for video_name, frame_number in missing_video_frames]
#         video_names = [video_name for video_name, frame_number in missing_video_frames]

#         # list_video_id = session.exec(
#         #     select(Video.id).where(Video.video_name.in_(video_names))
#         # ).all()

#         list_video = session.exec(
#             select(Video).where(Video.video_name.in_(video_names))
#         ).all()

#         list_video_id = [video.id for video in list_video]

#         video_name_id_dict = {video.id: video.video_name for video in list_video}

#         frames = session.exec(
#             select(Frame).where(Frame.frame_number.in_(frames_number),
#                                 Frame.video_id.in_(list_video_id))
#         ).all()

#         for frame in frames:
#             video_name = video_name_id_dict[frame.video_id]
#             key = f"frame:{video_name}-{frame.frame_number}"
#             redis_client.set(key, json.dumps(frame.to_dict()))
#             results_dict[(frame.video_name, frame.frame_number)] = frame


# #     print("missing frames: ")
# #     print(missing_video_frames)
# #     print("frame numbers")
# #     print(frames_number)
# #     print("list video id")
# #     print(list_video_id)
# #     print("frames: ")
# #     print(frames)
# #     frames_by_number = session.exec(
# #     select(Frame).where(Frame.frame_number.in_(frames_number))
# # ).all()
# #     print("Frames by number:", frames_by_number)
# #     frames_by_video = session.exec(
# #     select(Frame).where(Frame.video_id.in_(list_video_id))
# # ).all()
# #     print("Frames by video:", frames_by_video)

#     # frames = session.exec(
#     #     select(Frame).limit(100)
#     # ).all()
#     # print("frames: ")
#     # print(frames)

#     # Return results in the same order as the input frames_query
#     results = [results_dict[(video_name, frame_number)] for video_name, frame_number in frames_query if (video_name, frame_number) in results_dict]
#     # print("Results: ")
#     # print(results)
#     return results