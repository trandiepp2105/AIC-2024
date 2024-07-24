# some libs
from mmocr.apis import TextDetInferencer
from mmocr.utils.polygon_utils import poly2bbox
import matplotlib.pyplot as plt
from PIL import Image
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import cv2
import os
import json
from tqdm import tqdm

def extract_text_from_frame(frame_path,text_det,text_recog):
    filename, ext = os.path.splitext(os.path.basename(frame_path))
    result={filename:[]}
    # save image as array (H,W,C)
    image=cv2.imread(frame_path)[0:650]
    h=image.shape[0]
    w=image.shape[1]

    # detect text and find bounding box
    det_res=text_det(image,progress_bar=False,save_vis=True,out_dir='text_detect_restult')

    #get bounding box
    polygons=det_res['predictions'][0]['polygons']

    # regconize text in each box
    i=0
    for polygon in polygons:
        # find new bouding box which is rectangle
        bbox=poly2bbox(polygon)
        x_min,y_min,x_max,y_max=int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
        
        #padding bouding box
        padding=10 # amount paading each side
        y_min_padding=max(y_min-padding,0)
        y_max_padding=min(y_max+padding,h)
        x_min_padding=max(x_min-padding,0)
        x_max_padding=min(x_max+padding,w)

        # find roi
        roi=image[y_min_padding:y_max_padding,x_min_padding:x_max_padding]

        # gray scale
        gray_roi=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)

        text,score=text_recog.predict(Image.fromarray(gray_roi),return_prob=True)
        text_recog_result={"text":text,"score":score}
        result[filename].append(text_recog_result)
        cv2.imwrite(f'text_detect_restult/{filename}_{i}.jpg',gray_roi)
        i+=1
    return result

def OCR_from_folder(folder_path,det_model_name,recog_model_name,output_dir):
    # Create the directory
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print(f"Directory {output_dir} created successfully")

    #initalize text detection
    text_det=TextDetInferencer(model=det_model_name,device='cuda:0')

    # initial text regconition
    config = Cfg.load_config_from_name(recog_model_name)
    config['device']='cuda:0'
    text_recog = Predictor(config)
    # go through all video folder
    for video_folder in os.listdir(folder_path):
        video_folder_path=os.path.join(folder_path,video_folder)
        print(video_folder_path)
        # prepare to write into json file
        file_content={}
        if os.path.isfile(video_folder_path)==False:
            for frame in tqdm(os.listdir(video_folder_path)):
                frame_path=os.path.join(video_folder_path,frame)
                if os.path.isfile(frame_path) == True:
                    ocr_result=extract_text_from_frame(frame_path,text_det,text_recog)
                    file_content.update(ocr_result)
        with open(f'{output_dir}/{video_folder}.json','w') as f:
            json.dump(file_content,f,indent=4)


def main():
    OCR_from_folder('frames',det_model_name='textsnake_resnet50-oclip_fpn-unet_1200e_ctw1500',recog_model_name='vgg_seq2seq',output_dir='result')

main()
     