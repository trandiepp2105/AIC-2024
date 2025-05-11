import os
import torch
from torchvision import transforms
from PIL import Image
import cv2
import json
from ultralytics import YOLO
from configs import FRAME_WIDTH, FRAME_HEIGHT
import numpy as np

# Hàm để thay đổi kích thước ảnh
def resize_image(image, width, height):
    return cv2.resize(image, (width, height))

# # Hàm để chia ảnh thành các batch
# def divide_batches(folder_path, batch_size):
#     transform = transforms.Compose([
#         transforms.Resize((FRAME_HEIGHT, FRAME_WIDTH)),
#         transforms.ToTensor(),
#     ])

#     # Lấy danh sách các file ảnh
#     image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))]
#     num_batches = (len(image_files) + batch_size - 1) // batch_size
#     batches = []

#     for i in range(num_batches):
#         batch_files = image_files[i * batch_size:(i + 1) * batch_size]

#         # List để lưu trữ các tensor của từng ảnh trong batch
#         tensor_list = []
#         for file_name in batch_files:
#             image_path = os.path.join(folder_path, file_name)
#             img = Image.open(image_path)
#             img_tensor = transform(img)
#             tensor_list.append((file_name, img_tensor))

#         # Gộp các tensor vào một batch
#         batches.append(tensor_list)

#     return batches

# # Hàm để thực hiện phát hiện đối tượng trên từng batch ảnh
# def detect_objects(batch_tensor, model):
#     tensor_list = [item[1] for item in batch_tensor]
#     results = model(torch.stack(tensor_list))

#     detected_objects_batch = []

#     # Duyệt qua từng kết quả của từng ảnh trong batch
#     for i, result in enumerate(results):
#         detected_objects = {}

#         # Lấy danh sách tên lớp từ mô hình
#         class_names = model.names

#         # Khởi tạo danh sách rỗng cho mỗi lớp
#         for class_name in class_names:
#             detected_objects[model.names[class_name]] = []

#         # Xử lý từng kết quả phát hiện trong ảnh thứ i
#         for box in result.boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             score = float(box.conf[0])
#             class_id = int(box.cls[0])
#             class_name = model.names[class_id]

#             # Tạo key nếu chưa tồn tại
#             if class_name not in detected_objects:
#                 detected_objects[class_name] = []

#             # Thêm bounding box vào danh sách của lớp class_name
#             detected_objects[class_name].append({
#                 'bounding_box': {
#                     'x1': x1, 'y1': y1,
#                     'x2': x2, 'y2': y2
#                 },
#                 'score': score
#             })

#         # Thêm danh sách các đối tượng phát hiện được trong ảnh i vào batch kết quả
#         detected_objects_batch.append(detected_objects)

#     return detected_objects_batch

def divide_batches(folder_path, batch_size):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))]
    num_batches = (len(image_files) + batch_size - 1) // batch_size
    batches = []

    for i in range(num_batches):
        batch_files = image_files[i * batch_size:(i + 1) * batch_size]
        batches.append([(file_name, os.path.join(folder_path, file_name)) for file_name in batch_files])

    return batches

def detect_objects(batch_files, model):
    transform = transforms.Compose([
        transforms.Resize((640, 480)),
        transforms.ToTensor(),
    ])

    tensor_list = []
    for file_name, file_path in batch_files:
        img = Image.fromarray(cv2.imread(file_path))
        img_tensor = transform(img)
        tensor_list.append((file_name, img_tensor))

    results = model(torch.stack([item[1] for item in tensor_list]), verbose=False)

    detected_objects_batch = []

    # Duyệt qua từng kết quả của từng ảnh trong batch
    for i, result in enumerate(results):
        detected_objects = {}

        # Lấy danh sách tên lớp từ mô hình
        class_names = model.names

        # Khởi tạo danh sách rỗng cho mỗi lớp
        for class_name in class_names:
            detected_objects[model.names[class_name]] = []

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

def generate_output_json(folder_path, output_directory, model_path='yolov8m.pt', batch_size=64, model_dir='data/models_yolo'):
    model_path = os.path.join(model_dir, model_path)
    
    model = YOLO(model_path, verbose=False)
    model.save(model_path)
  
    for subdir_name in os.listdir(folder_path):
        subdir_path = os.path.join(folder_path, subdir_name)
        if os.path.isdir(subdir_path):
            video_output_directory = os.path.join(output_directory, subdir_name)
            os.makedirs(video_output_directory, exist_ok=True)

            detections_per_frame = process_frames(subdir_path, model, batch_size)

            if detections_per_frame:
                for frame_id, frame_detections in detections_per_frame.items():
                    json_filename = f"{frame_id}.json"
                    numpy_filename = f"{frame_id}.npy"
                    output_json = os.path.join(video_output_directory, json_filename)
                    output_numpy = os.path.join(video_output_directory, numpy_filename)
                    vector_count = [obj['count'] for obj in frame_detections.values()]
                    np.save(output_numpy, np.array(vector_count, dtype=np.float32))
                    detection = {
                        'info': frame_detections,
                        'vector_count': vector_count
                    }
                    with open(output_json, 'w') as f:
                        json.dump(detection, f, indent=4)

                torch.cuda.empty_cache()

            print(f"Object detection results for video {subdir_name} have been saved to JSON files.")

    print("Object detection results have been saved to JSON files.")

# if __name__ == '__main__':
#     # Thư mục chứa các frame cần phát hiện đối tượng
#     frame_folder = r'C:\AIC-2024-DATA\frames'

#     # Thư mục chứa kết quả phát hiện đối tượng
#     output_directory = r'C:\AIC-2024-DATA\objects'

#     # Thực hiện phát hiện đối tượng và lưu kết quả vào các file JSON
#     generate_output_json(frame_folder, output_directory, 'yolov8m.pt', 64)
