import os
import torch
import time
import csv
from torchvision import transforms
from PIL import Image
import cv2
import json
from ultralytics import YOLO

# Định nghĩa kích thước mới cho frame
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Đường dẫn đến thư mục chứa các ảnh
folder_path = os.path.join(os.path.dirname(__file__), "frames")

# Tải mô hình YOLOv8
models = {
    'yolov8n': YOLO('yolov8n.pt')
}

# Hàm để thay đổi kích thước ảnh
def resize_image(image, width, height):
    return cv2.resize(image, (width, height))

# Hàm để chia ảnh thành các batch
def divide_batches(folder_path, batch_size):
    transform = transforms.Compose([
        transforms.Resize((FRAME_HEIGHT, FRAME_WIDTH)),
        transforms.ToTensor(),
    ])

    # Lấy danh sách các file ảnh
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))]
    num_batches = (len(image_files) + batch_size - 1) // batch_size
    batches = []

    for i in range(num_batches):
        batch_files = image_files[i * batch_size:(i + 1) * batch_size]

        # List để lưu trữ các tensor của từng ảnh trong batch
        tensor_list = []
        for file_name in batch_files:
            image_path = os.path.join(folder_path, file_name)
            img = Image.open(image_path)
            img_tensor = transform(img)
            tensor_list.append((file_name, img_tensor))

        # Gộp các tensor vào một batch
        batches.append(tensor_list)

    return batches

# Hàm để thực hiện phát hiện đối tượng trên từng batch ảnh
def detect_objects(batch_tensor, model):
    tensor_list = [item[1] for item in batch_tensor]
    results = model(torch.stack(tensor_list))

    detected_objects_batch = []

    # Duyệt qua từng kết quả của từng ảnh trong batch
    for i, result in enumerate(results):
        detected_objects = {}

        # Lấy danh sách tên lớp từ mô hình
        class_names = model.names

        # Khởi tạo danh sách rỗng cho mỗi lớp
        for class_name in class_names:
            detected_objects[class_name] = []

        # Xử lý từng kết quả phát hiện trong ảnh thứ i
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

        # Thêm danh sách các đối tượng phát hiện được trong ảnh i vào batch kết quả
        detected_objects_batch.append(detected_objects)

    return detected_objects_batch

def process_frames(frame_dir, model, batch_size=16):
    batches = divide_batches(frame_dir, batch_size)
    all_detections = {}

    for batch in batches:
        torch.cuda.empty_cache()

        detected_objects_batch = detect_objects(batch, model)

        for (file_name, _), detections in zip(batch, detected_objects_batch):
            frame_id = os.path.splitext(file_name)[0]  # Lấy tên file làm frame_id
            frame_detections = {}

            for class_name, objects in detections.items():
                class_bb_list = []

                for obj in objects:
                    bounding_box = obj['bounding_box']
                    score = obj['score']
                    class_bb_list.append([
                        bounding_box['x1'], bounding_box['y1'], bounding_box['x2'], bounding_box['y2'], score
                    ])

                frame_detections[class_name] = {
                    'count': len(class_bb_list),
                    'objects': class_bb_list
                }

            all_detections[frame_id] = frame_detections

    return all_detections

root_directory = os.path.dirname(folder_path)
output_directory = os.path.join(os.path.dirname(__file__), "Object-Detections")
os.makedirs(output_directory, exist_ok=True)

# Chỉ định kích thước batch
batch_size = 32

# Duyệt qua từng thư mục con trong thư mục gốc
for subdir_name in os.listdir(folder_path):
    subdir_path = os.path.join(folder_path, subdir_name)
    if os.path.isdir(subdir_path):
        # Tạo thư mục cho từng video trong thư mục output
        video_output_directory = os.path.join(output_directory, subdir_name)
        os.makedirs(video_output_directory, exist_ok=True)
        
        for model_name, model in models.items():
            # Thực hiện object detection trên tất cả các hình ảnh trong thư mục con
            detections_per_frame = process_frames(subdir_path, model, batch_size)
            
            if detections_per_frame:
                for frame_id, frame_detections in detections_per_frame.items():
                    # Tạo tên file JSON từ tên frame
                    json_filename = f"{frame_id}.json"
                    output_json = os.path.join(video_output_directory, json_filename)

                    # Ghi danh sách các đối tượng được phát hiện vào file JSON
                    with open(output_json, 'w') as f:
                        json.dump(frame_detections, f, indent=4)
                        print(f"Saved detections for frame {frame_id} in {json_filename}")

        torch.cuda.empty_cache()

print("Object detection results have been saved to JSON files.")
