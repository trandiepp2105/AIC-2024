
# from sqlmodel import select, Session
# from typing import List, Any

# import logging
# from pathlib import Path
# import sys
# current_dir = Path(__file__).resolve().parent
# app_dir = current_dir / '../app'
# sys.path.append(str(app_dir))

# from app.api.deps import SessionDep
# from app.models import Frame


# logging.error("ERROR")
# def get_frame(session: Session) -> Any:
#     """
#     Retrieve frames
#     """
#     statement = select(Frame)
#     results = session.exec(statement).all()
#     with open("backend/result", "rt") as f:
#         f.write(results)
#     return results

# frames = get_frame(SessionDep)

# logging.warning("frames: ")
# logging.warning(frames)

def create_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"File {file_path} đã được tạo thành công.")

# Ví dụ: tạo file mới với nội dung
create_file('example.txt', 'Đây là nội dung của file mới.')