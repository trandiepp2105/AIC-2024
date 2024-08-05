import yt_dlp as youtube_dl

def download_youtube_video(url, output_path='.'):
    try:
        ydl_opts = {
            'format': 'best[height<=1440]', # Chất lượng video tải về
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Download completed! Video saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# URL của video YouTube
video_url = 'https://www.youtube.com/watch?v=c6r_j-3nXMI'
# Đường dẫn lưu video
output_path = './Download_video/videos'

# Gọi hàm để tải video
download_youtube_video(video_url, output_path)
