import re
import os
import zipfile
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests.exceptions import RequestException
from multiprocessing import Pool
from configs import BASE_FOLDER

# URL của Google Sheets
url = 'https://docs.google.com/spreadsheets/d/1mO3zS79L1HMLZ-BLpyy8E-n9RROOElms5DS_Gi1gKiU/edit?gid=0#gid=0'

# Trích xuất ID từ URL
SPREADSHEET_ID = re.search(r'/d/([a-zA-Z0-9-_]+)', url).group(1)

# Xác thực và khởi tạo API Sheets và Drive
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 
          'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = './gg-sheet-credentials.json'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

sheets_service = build('sheets', 'v4', credentials=credentials)

# Vùng dữ liệu cần lấy từ Sheets
RANGE_NAME = 'A2:E'

def fetch_data_from_sheet():
    try:
        # Gọi API Sheets để lấy dữ liệu từ bảng tính
        sheet = sheets_service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get('values', [])
        print("Truy cập sheet thành công!")
        return values
    except HttpError as err:
        print(f"Đã xảy ra lỗi HTTP: {err}")
    except RequestException as err:
        print(f"Đã xảy ra lỗi yêu cầu: {err}")
    except Exception as err:
        print(f"Đã xảy ra lỗi không xác định: {err}")
    return []

def download_and_extract(args):
    row, base_folder = args
    file_type = row[0]
    filename = row[1]
    direct_link = row[4]
    
    if file_type == 'Video':
        dest_folder = os.path.join(base_folder, 'videos')
    elif file_type == 'Keyframe':
        return
        dest_folder = os.path.join(base_folder, 'keyframes')
    else:
        print(f"Loại tệp không hợp lệ: {file_type}")
        return

    # Tạo thư mục đích nếu chưa tồn tại
    os.makedirs(dest_folder, exist_ok=True)
    
    # Tải file về
    try:
        print(f"Tải {filename} từ {direct_link} vào {dest_folder}...")
        response = requests.get(direct_link, stream=True)
        response.raise_for_status()  # Đảm bảo phản hồi HTTP thành công
        file_path = os.path.join(dest_folder, filename)

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                
        print(f"Đã tải {filename} vào {dest_folder}")

        # Giải nén file nếu là zip
        if filename.endswith('.zip'):
            print(f"Giải nén {filename} tại {dest_folder}...")
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(dest_folder)

            print(f"Đã giải nén {filename} tại {dest_folder}")
            
            # Xóa file zip sau khi đã giải nén
            os.remove(file_path)
            print(f"Đã xóa file {filename} sau khi giải nén")
    except RequestException as err:
        print(f"Đã xảy ra lỗi yêu cầu khi tải {filename}: {err}")
    except zipfile.BadZipFile as err:
        print(f"Đã xảy ra lỗi khi giải nén {filename}: {err}")
    except Exception as err:
        print(f"Đã xảy ra lỗi không xác định khi xử lý {filename}: {err}")

if __name__ == '__main__':
    base_folder = BASE_FOLDER
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
    os.makedirs(os.path.join(base_folder, 'videos'), exist_ok=True)
    os.makedirs(os.path.join(base_folder, 'keyframes'), exist_ok=True)

    values = fetch_data_from_sheet()
    
    # Chuẩn bị dữ liệu cho multiprocessing
    data_for_pool = [(row, base_folder) for row in values]

    # Sử dụng multiprocessing để tải và giải nén các tệp song song
    with Pool(processes=6) as pool:
        pool.map(download_and_extract, data_for_pool)

    print('Tất cả các file đã được tải và giải nén thành công.')
