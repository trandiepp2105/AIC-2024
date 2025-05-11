import os
import json

def addFPS(json_path, fps):
    new_json = {}
    with open(json_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for frame_number, v in data.items():
            new_json[frame_number] = {
                'text': v,
                'fps': fps
            }

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(new_json, json_file, ensure_ascii=False, indent=4)

def dictFPS(csv_path):
    fps_dict = {}
    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        for line in csv_file:
            line = line.strip()
            if not line:
                continue
            video_name, fps = line.split(',')
            fps_dict[video_name] = fps

    return fps_dict

def addFPSForAllJson(json_folder, fps_):
    i = 0
    for root, _, files in os.walk(json_folder):
        for file in files:
            if not file.endswith('.json'):
                continue
            json_path = os.path.join(root, file)
            video_name = os.path.basename(json_path).split('.')[0]
            if video_name in fps_:
                i += 1
                print(f'{i}. Add FPS for {video_name}')
                fps = fps_[video_name]
                addFPS(json_path, fps)

if __name__ == '__main__':
    json_folder = r"C:\Users\hokha\OneDrive\Desktop\storage\elastic-json\elastic-json"
    csv_path = r"E:\videos.csv"
    dictPFSs = dictFPS(csv_path)
    addFPSForAllJson(json_folder, dictPFSs)
    print('Done')