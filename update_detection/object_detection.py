import os
import torch
from torchvision import transforms
from PIL import Image
import cv2
import json
#from configs import FRAME_WIDTH, FRAME_HEIGHT
import numpy as np

# Hàm để thay đổi kích thước ảnh
def resize_image(image, width, height):
    return cv2.resize(image, (width, height))

# Hàm chia ảnh thành các batch
def divide_batches(folder_path, batch_size):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))]
    num_batches = (len(image_files) + batch_size - 1) // batch_size
    batches = []

    for i in range(num_batches):
        batch_files = image_files[i * batch_size:(i + 1) * batch_size]
        batches.append([(file_name, os.path.join(folder_path, file_name)) for file_name in batch_files])

    return batches

# Hàm chuyển đổi box định dạng cxcywh sang xyxy
def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h),
         (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)

# Hàm rescale box từ [0; 1] sang kích thước ảnh
def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b

def detect_objects(batch_files, model):
    transform = transforms.Compose([
        transforms.Resize((640, 480)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    tensor_list = []
    for file_name, file_path in batch_files:
        img = Image.open(file_path)
        img_tensor = transform(img).unsqueeze(0)  # Thêm chiều batch-size
        tensor_list.append((file_name, img_tensor))

    detected_objects_batch = []

    for file_name, img_tensor in tensor_list:
        outputs = model(img_tensor)

        probas = outputs['pred_logits'].softmax(-1)[0, :, :-1]
        keep = probas.max(-1).values > 0.9 # Lấy các bounding box có xác suất lớn hơn 0.9

        bboxes_scaled = rescale_bboxes(outputs['pred_boxes'][0, keep].cpu(), img_tensor.shape[-2:])

        CLASSES = [
            'N/A', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
            'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A',
            'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
            'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack',
            'umbrella', 'N/A', 'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
            'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
            'skateboard', 'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass',
            'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich',
            'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
            'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table', 'N/A',
            'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
            'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A',
            'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
            'toothbrush'
        ]

        detected_objects = {class_name: {'count': 0, 'objects': []} for class_name in CLASSES if class_name != 'N/A'}

        for p, (xmin, ymin, xmax, ymax) in zip(probas[keep], bboxes_scaled.tolist()):
            cl = p.argmax().item()
            class_name = CLASSES[cl]
            if class_name != 'N/A':  # Bỏ qua lớp 'N/A'
                bbox = [xmin, ymin, xmax, ymax, float(p[cl])]

                detected_objects[class_name]['objects'].append({
                    'bounding_box': bbox[:4],
                    'score': bbox[4]
                })
                detected_objects[class_name]['count'] += 1

        detected_objects_batch.append(detected_objects)

    return detected_objects_batch

# Hàm xử lý tất cả các frame trong một thư mục
def process_frames(frame_dir, model, batch_size=16):
    batches = divide_batches(frame_dir, batch_size)
    all_detections = {}

    for batch in batches:
        torch.cuda.empty_cache()

        detected_objects_batch = detect_objects(batch, model)

        for (file_name, _), detections in zip(batch, detected_objects_batch):
            frame_id = os.path.splitext(file_name)[0]
            frame_detections = {}

            for class_name, objects in detections.items():
                class_bb_list = []

                for obj in objects['objects']:
                    bounding_box = obj['bounding_box']
                    score = obj['score']
                    class_bb_list.append([
                    bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3], score
                    ])

                frame_detections[class_name] = {
                    'count': len(class_bb_list),
                    'objects': class_bb_list
                }

            all_detections[frame_id] = frame_detections

    return all_detections

# Hàm sinh ra các tệp JSON và NumPy
def generate_output_json(folder_path, output_directory, model_path='model/detr_resnet101.pth', batch_size=64):
    model = torch.hub.load('facebookresearch/detr', 'detr_resnet101', pretrained=False)
    model.load_state_dict(torch.load(model_path))
    model.eval()

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


# Hàm chính
# if __name__ == '__main__':
#     # Thư mục chứa các frame cần phát hiện đối tượng
#     frame_folder = r'C:\AIC-2024-DATA\frames'

#     # Thư mục chứa kết quả phát hiện đối tượng
#     output_directory = r'C:\AIC-2024-DATA\objects'

#     # Thực hiện phát hiện đối tượng và lưu kết quả vào các file JSON
#     generate_output_json(frame_folder, output_directory, 'yolov8m.pt', 64)
