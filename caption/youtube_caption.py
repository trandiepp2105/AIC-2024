# Du lieu input gom list cac dict {'name': video_name, 'url': video_url}

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
            translation_result=get_translated_transcript(id,code_lang)

            #nếu vẫn không thể dịch được thì ta chấp nhận không video không có caption theo code_lang
            if translation_result == None :
                result[id]=translation_result
            else:
                result[id]=translation_result.fetch()
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
    vi_code='vi'
    en_code='en'
    
    if batch_size == None:
        batch_size=len(data)
    total_batches=ceil(len(data)/batch_size)
    # chạy từng batch
    for i in range(0,len(data),batch_size):
        print(f"Batch : {i//batch_size+1}/{total_batches} | Batch size : {min(i+batch_size,len(data))-i}")
        # lấy ra id của mỗi batch từ url
        video_ids=[extract_youtube_id(i['url'] )for i in data[i:i+batch_size]]
        
        # trích caption tiếng Việt
        vi_captions=get_caption_from_list_ids(video_ids=video_ids,code_lang=vi_code)
        # trích caption tiếng Anh
        en_captions=get_caption_from_list_ids(video_ids=video_ids,code_lang=en_code)
        
        # ghi caption vào file json
        for video in tqdm(data[i:i+batch_size]):
            # file vi
            file_name=video['name']+'_vi'
            write_caption_to_json(caption=vi_captions[extract_youtube_id(video['url'])],file_name=file_name,out_dir=out_dir)
            
            # file en
            file_name=video['name']+'_en'
            write_caption_to_json(caption=en_captions[extract_youtube_id(video['url'])],file_name=file_name,out_dir=out_dir)



data=[
    {"name" : "Đơn Giản Hóa #136 Nói Dối" , "url":"https://youtu.be/Eefj-w-pm-w?si=QqI9pi4ANXBOo_zV"},
    {'name' : 'Tất cả các biện pháp thao túng tâm lý trong 6 phút' , 'url' : 'https://youtu.be/roTAANuN1Yc?si=vbPe9lYh2Hy4fxBJ'},
    {'name' : 'Tất cả xu hướng tính dục trong 7 phút' , 'url' : 'https://youtu.be/vWfEHLo-wRM?si=5iM8FQoGUgaUc7Dm'},
    {'name' : 'Đơn Giản Hóa #134 Thời Tiết' , 'url' : 'https://youtu.be/zKyByQbqjpc?si=DZ8dsD-ACazMtf2H'},
    {'name' : 'Đơn giản hóa #132 Ronaldo' , 'url' : 'https://youtu.be/TcCNoSGQb2o?si=8-XGSMBKCm-gmWcc'},
    {'name' : 'Đơn giản hóa #115 Harry Potter' , 'url' : 'https://youtu.be/OAwAK5vjpEo?si=Pgc2NsU19Y8xhHSz'},
    ]

extract_caption_from_data(data,out_dir="result")