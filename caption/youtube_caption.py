# Du lieu input gom list cac dict {'name': video_name, 'url': video_url}

from youtube_transcript_api import YouTubeTranscriptApi, Transcript
from youtube_transcript_api._errors import *
import json
import os


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

    :return: caption của các id 
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
                result[id]=[]
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
    if ".json" not in file_name :
        file_name=file_name + ".json"
    file_path=os.path.join(out_dir,file_name)

    with open(file_path,'w') as json_file:
        json.dump(caption,json_file,indent=4)