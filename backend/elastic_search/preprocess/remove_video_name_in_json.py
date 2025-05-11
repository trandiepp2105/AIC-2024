import os
import json

# Function to update JSON keys and write back to the file
def update_json_file(file_path):
    # Load the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Remove non-numeric characters from each key
    updated_data = {''.join(filter(str.isdigit, key)): value for key, value in data.items()}
    
    # Write the updated data back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    ocr_json_folder = os.getenv('CONTAINER_OCR_JSON_DATA_FOLDER')
    for filename in os.listdir(ocr_json_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(ocr_json_folder, filename)
            update_json_file(file_path)