from youtube_transcript_api import YouTubeTranscriptApi, Transcript
from youtube_transcript_api._errors import *
import json
import os
from pytube import YouTube
from tqdm import tqdm
from math import ceil


def get_first_transcript(transcript_list):
    """
    Trích đối tượng transcipt đầu tiên trong transcript list

    :param transcript_list: đối tượng TranscriptList từ 1 video
    :type transcript_list: TranscriptList

    :return: đối tượng Transcript đầu tiên có trong transcript_list
    :rtype: Transcript
    """

    for transcript in transcript_list:
        return transcript
    
def get_list_code_translatable_languages(transcript_list):
    """
    Lấy ra list các code của các ngôn ngữ có thể dịch từ transcript sang

    :param transcript_list: đối tượng TranscriptList từ 1 video
    :type transcript_list: TranscriptList

    :return: list các code ngôn ngữ
    :rtype: list[str]
    """
    translation_languages=transcript_list._translation_languages

    code=[i['language_code'] for i in translation_languages]

    return code

def get_translated_transcript(video_id,code_lang):
    """ 
    Lấy ra đối tượng Transcript được dịch từ video_id sang ngôn ngữ có code_lang
    Chú ý: nếu transcript theo code_lang đã có sẵn mà vẫn dùng translate thì sẽ dẫn đến kết quả tệ

    :param video_id: id của video trên Youtube
    :type video_id: str
    :param code_lang: code của ngôn ngữ
    :type code_lang: str

    :return: đối tượng Transcript sau khi dịch, None nếu không dịch được
    :rtype: Transcript object
    """

    # lấy list transcript của video 
    # từ đó ta có thể lấy được danh sách các ngôn ngữ có thể dịch
    transcript_list=YouTubeTranscriptApi.list_transcripts(video_id)

    #kiểm tra có thể dịch sang code_lang không
    if code_lang not in get_list_code_translatable_languages(transcript_list):
        return None
    
    #trả vể đối tượng Transcript sau khi đã dịch
    return get_first_transcript(transcript_list).translate(code_lang)

def get_caption_from_list_ids(video_ids,code_lang):

    """
    Lấy ra các caption từ list video ids

    :param video_ids: danh sách các id của video trên Youtube
    :type video_ids: list[str]
    :param code_lang: code của ngôn ngữ
    :type code_lang: str

    :return: caption của các id , id nào không có caption sẽ có giá trị None
    :rtype: { str:[ { 'text' : str, 'start' : float, 'duration' : float },... ],... }
    """
    
    #lấy caption có sẵn , ưu tiên caption được tạo tay (manually created)
    #fail dùng để lưu các id không có caption có sẵn theo code_lang
    result,fail=YouTubeTranscriptApi.get_transcripts(video_ids=video_ids,languages=[code_lang],continue_after_error=True)

    # kiểm tra có id nào bị fail không
    # nếu có thì ta sẽ xử lí bằng cách dịch qua code_lang
    # chính vì dịch qua nên sẽ tốn thời gian hơn do không dùng được batch
    if len(fail) > 0:
        for id in fail:
            try:
                translation_result=get_translated_transcript(id,code_lang)

                #nếu vẫn không thể dịch được thì ta chấp nhận không video không có caption theo code_lang
                if translation_result == None :
                    result[id]=translation_result
                else:
                    result[id]=translation_result.fetch()
            except:
                result[id]=[]
    return result
def write_caption_to_json(caption,file_name,out_dir=""):
    """
    Ghi caption vào file json trong out_dir

    :param caption: caption của video
    :type caption: [ { 'text' : str, 'start' : float, 'duration' : float },... ]
    :param file_name: tên của file sẽ lưu 
    :type file_name: str
    :param out_dir: path tới thư mục lưu
    :type out_dir: str 
    """
    
    # kiểm tra folder đã tồn tại chưa
    # nếu chưa tồn tại thì tạo folder
    if out_dir!="" :
        try:
            os.makedirs(out_dir)
        except FileExistsError:
            pass
        
    if ".json" not in file_name :
        file_name=file_name + ".json"
    file_path=os.path.join(out_dir,file_name)

    with open(file_path,'w',encoding='utf-8') as json_file:
        json.dump(caption,json_file,ensure_ascii=False,indent=4)

def extract_youtube_id(url):
    """
    Lấy ra id của video từ url

    :param url: url của video
    :type url: str

    :return: id của video
    :rtype: str 
    """
    # tạo đối tượng Youtube từ url
    yt = YouTube(url)
    
    # lấy thuộc tính id của đối tượng và trả về
    video_id = yt.video_id
    
    return video_id

def add_endtime_to_caption(caption):
    """
    Thêm frame number vào caption

    :param caption: caption của video
    :type caption: [ { 'text' : str, 'start' : float, 'duration' : float },... ]
    :param fps: số frame trên giây của video

    :return: caption sau khi thêm frame number
    :rtype: [ { 'text' : str, 'start' : float, 'duration' : float, 'frame_number' : int },... ]
    """

    if caption == None:
        return []

    for i in range(len(caption)):
        caption[i]['end']=caption[i]['start']+caption[i]['duration']
    return caption

def extract_caption_from_data(data,batch_size=50,out_dir=""):
    """
    Làm task chính, từ data, trích xuất ra được các file json chứa caption của các video trong data theo tiếng anh và tiếng việt
    
    :param data: data được truyền vào gồm danh sách thông tin của các video
    :type data: list[{"name" : str, "url" : str }]
    :param out_dir: đường dẫn tới thư mục lưu các file
    :type out_dir: str
    :param batch_size: kích thước mỗi batch, nếu chỉ có 1 batch thì batch_size=None
    :type batch_size: int
    """

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    vi_code='vi'
    
    if batch_size == None:
        batch_size=len(data)
    total_batches=ceil(len(data)/batch_size)
    # chạy từng batch
    for i in range(0,len(data),batch_size):
        print(f"Batch : {i//batch_size+1}/{total_batches} | Batch size : {min(i+batch_size,len(data))-i}")
        # lấy ra id của mỗi batch từ url
        video_ids=[extract_youtube_id(i['watch_url'] )for i in data[i:i+batch_size]]
        
        # trích caption tiếng Việt
        vi_captions=get_caption_from_list_ids(video_ids=video_ids,code_lang=vi_code)

        # ghi caption vào file json
        for video in tqdm(data[i:i+batch_size]):
            # file vi
            file_name=video['name']
            vie_captions=add_endtime_to_caption(vi_captions[extract_youtube_id(video['watch_url'])])
            write_caption_to_json(caption=vie_captions,file_name=file_name,out_dir=out_dir)

import pandas as pd
from collections import deque

def wfile(folder, end):
    list_file = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(end):
                list_file.append(os.path.join(root, file))
    return list_file

def frame_caption(csv_path, caption_path, output_dir, video_name, time = 5):
    print(f'Processing {video_name}...')
    df = pd.read_csv(csv_path)
    with open(caption_path, 'r', encoding='utf-8') as json_file:
        caption = json.load(json_file)

    caption = sorted(caption, key=lambda x: x['start'])

    ct = deque()
    now = 0

    list_caption = {}
    
    for i in range(len(df)):
        row = df.iloc[i]
        second = row['second']
        frame_number = row['frame_number']
        start = second - time
        end = second + time

        while len(ct) > 0 and ct[0][0] < start:
            ct.popleft()

        while now < len(caption) and caption[now]['start'] < end:
            ct.append((caption[now]['end'], caption[now]['text']))
            now += 1

        cap = ' '.join(list(map(lambda x: x[1], ct))) if len(ct) > 0 else ''

        list_caption[f'{int(frame_number)}'] = cap

    with open(os.path.join(output_dir, video_name + '.json'), 'w', encoding='utf-8') as json_file:
        json.dump(list_caption, json_file, ensure_ascii=False, indent=4)
    print(f'Finish {video_name}...')

from multiprocessing import Pool

def extract_caption_frame(csv_folder, caption_folder, output_folder):
    list_file = wfile(csv_folder, ".csv")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    list_agrs = []
    for file in list_file:
        name = os.path.basename(file).split(".")[0]
        list_agrs.append((file, os.path.join(caption_folder, name + ".json"), output_folder, name))

    with Pool() as p:
        p.starmap(frame_caption, list_agrs)

if __name__ == '__main__':
    metadata_folder = r"C:\Users\hokha\OneDrive\Desktop\storage\media-info"
    out_dir = r'C:\Users\hokha\OneDrive\Desktop\storage\captions_yt'

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    batch_size = 100

    list_json = [os.path.join(metadata_folder, i) for i in os.listdir(metadata_folder) if i.endswith('.json')]
    list_data = []
    for json_file in list_json:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data['name'] = os.path.basename(json_file).split('.')[0]
            list_data.append(data)
    # extract_caption_from_data(list_data, batch_size, out_dir)

    csv_folder = r'C:\Users\hokha\OneDrive\Desktop\storage\csv'
    caption_folder = r'C:\Users\hokha\OneDrive\Desktop\storage\captions'

    if not os.path.exists(caption_folder):
        os.makedirs(caption_folder)

    extract_caption_frame(csv_folder, out_dir, caption_folder)