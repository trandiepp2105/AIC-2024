import yt_dlp as youtube_dl
import os

def download_youtube_video(video_info, output_path='.'):
    try:
        ydl_opts = {
            'format': 'best[height<=1440]', # Chất lượng video tải về
            "outtmpl": f"{output_path}/{video_info['name']}.%(ext)s", # Đường dẫn lưu video
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_info['url']])
        print(f"Download completed! Video saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# URL của video YouTube
videos = [
    {"url": "https://www.youtube.com/watch?v=E5Sj7BWA8zE", "name": "L01"},
    {"url": "https://www.youtube.com/watch?v=2TjCNNLAS0s", "name": "L02"},
    {"url": "https://www.youtube.com/watch?v=mnLf6ME61M4", "name": "L04"},
    {"url": "https://www.youtube.com/watch?v=7MB7PzlGBL4", "name": "L05"},
    {"url": "https://www.youtube.com/watch?v=K8B97eIyYlw", "name": "L06"},
    {"url": "https://www.youtube.com/watch?v=jbCy6kzmTSo", "name": "L07"},
    {"url": "https://www.youtube.com/watch?v=uBOFg468uf8", "name": "L10"},
    {"url": "https://www.youtube.com/watch?v=tXj2YiVLN8I", "name": "L11"},
    {"url": "https://www.youtube.com/watch?v=mk2fM5bf2sE", "name": "L13"},
    {"url": "https://www.youtube.com/watch?v=zGJlmLBiu5w", "name": "L15"},
    {"url": "https://www.youtube.com/watch?v=k2u1n_Jb7NA", "name": "L18"},
    {"url": "https://www.youtube.com/watch?v=_qjksIwX_jc", "name": "L20"},
    {"url": "https://www.youtube.com/watch?v=JxQG847sc38", "name": "L21"},
    {"url": "https://www.youtube.com/watch?v=YZDC4GgSNxA", "name": "L22"},
    {"url": "https://www.youtube.com/watch?v=om2BlyskNm0", "name": "L23"},
    {"url": "https://www.youtube.com/watch?v=mFDnD8R3MZE", "name": "L26"},
    {"url": "https://www.youtube.com/watch?v=i6xWkimcz8s", "name": "L29"},
    {"url": "https://www.youtube.com/watch?v=s3JG0j0qq-k", "name": "L31"},
    {"url": "https://www.youtube.com/watch?v=li9GiFP3cKI", "name": "L37"}
]
# Đường dẫn lưu video
output_path = r"/storage/videos"

if not os.path.exists(output_path):
    os.makedirs(output_path)

for video in videos:
    download_youtube_video(video, output_path)