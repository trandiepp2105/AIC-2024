import cv2
import os
import json
from ultralytics import YOLO


model = YOLO('yolov8m.pt')  

# Hàm để thực hiện phát hiện đối tượng
def detect_objects(image):
    results = model(image)  # Thực hiện phát hiện đối tượng

    detected_objects = {}

    # Lấy danh sách tên lớp từ mô hình
    class_names = model.names

    # Khởi tạo danh sách rỗng cho mỗi lớp
    for class_name in class_names:
        detected_objects[model.names[class_name]] = []

    # Xử lý từng kết quả phát hiện
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            score = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            
            # Tạo key nếu chưa tồn tại
            if class_name not in detected_objects:
                detected_objects[class_name] = []

            # Thêm bounding box vào danh sách của lớp class_name
            detected_objects[class_name].append({
                'bounding_box': {
                    'x1': x1, 'y1': y1,
                    'x2': x2, 'y2': y2
                },
                'score': score
            })

    return detected_objects


# Hàm để xử lý các frame hình ảnh
def process_frames(frame_dir):
    frame_files = [f for f in os.listdir(frame_dir) if f.endswith(('.jpg', '.png'))]
    all_detections = {}

    for frame_file in frame_files:
        image_path = os.path.join(frame_dir, frame_file)
        if not os.path.exists(image_path):
            print(f"File does not exist: {image_path}")
            continue
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to read image: {image_path}")
            continue

        detections = detect_objects(image)

        # Tính số lượng đối tượng và lưu vào all_detections theo frame_id
        frame_id = os.path.splitext(frame_file)[0]  # Lấy tên frame mà không có phần mở rộng
        frame_detections = {}

        for class_name, objects in detections.items():
            count = len(objects)
            frame_detections[class_name] = {
                'count': count,
                'objects': objects
            }

        all_detections[frame_id] = frame_detections

    return all_detections

# Đường dẫn tới thư mục chứa các frame hình ảnh
root_directory = r'frames\frames'  # Đường dẫn với chuỗi thô (raw string)

# Thư mục để lưu các file JSON
output_directory = os.path.join(os.path.dirname(root_directory), 'Object-Detections')
os.makedirs(output_directory, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

# Duyệt qua từng thư mục con và xử lý frame hình ảnh
for subdir in os.listdir(root_directory):
    subdir_path = os.path.join(root_directory, subdir)
    if os.path.isdir(subdir_path):
        detections_per_frame = process_frames(subdir_path)

        # Tạo tên file JSON từ tên thư mục chứa frame hình ảnh
        json_filename = subdir + '.json'
        output_json = os.path.join(output_directory, json_filename)

        # Ghi danh sách các đối tượng được phát hiện vào file JSON
        with open(output_json, 'w') as f:
            json.dump(detections_per_frame, f, indent=4)

        print(f"Detections for {subdir} have been saved to {output_json}")
