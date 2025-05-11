from onedrivedownloader import download
import os
# from configs import *

def download_from_onedrive(url, output_folder,  filename = 'data.zip'):
    print(f'Download {filename} from {url}')
    download(url, filename, unzip=True, unzip_path=output_folder, clean=True)
    print(f'Download {filename} done')

if __name__ == '__main__':
    # csv_url = CSV_URL
    # keyframes_url = KEYFRAMES_URL

    # root = ROOT_DIR

    # download_from_onedrive(csv_url, root)
    # download_from_onedrive(keyframes_url, root)

    root = '/storage'
    
    if not os.path.exists(root):
        os.makedirs(root)

    data_url = 'https://studenthcmusedu-my.sharepoint.com/:u:/g/personal/22120076_student_hcmus_edu_vn/EYDriMTjtWNMgpr_TikLZAMBhQxFtuaVezD7t2Gub_zbEw?e=BtrMPH&download=1'
    download_from_onedrive(data_url, root, 'db.zip')

    video_url = 'https://studenthcmusedu-my.sharepoint.com/:u:/g/personal/22120076_student_hcmus_edu_vn/EdGiZtr3XTNAnv4QTjVgWxoBrAXtBjF4WGNYlIjUIJ5RtA?e=dFiL1j&download=1'
    download_from_onedrive(video_url, root, 'videos.zip')

    # elastic_url = 'https://studenthcmusedu-my.sharepoint.com/:u:/g/personal/22120076_student_hcmus_edu_vn/EXfSJcgPzwxLkbaTpJOjF_MBmvq-l2hsJc6fbp7viVf0eg?e=NJrrEN&download=1'
    # download_from_onedrive(elastic_url, root, 'elastic.zip')

    elastic_json_url = 'https://studenthcmusedu-my.sharepoint.com/:u:/g/personal/22120076_student_hcmus_edu_vn/EWhV7paRgOVChfd6BVQsA4sBPvDdz6xM6zWeg8WpSHCRwA?e=vN6nkO&download=1'
    download_from_onedrive(elastic_json_url, root, 'elastic-json.zip')
    print('Download done')