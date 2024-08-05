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
import numpy as np
import math
import torch



def do_padding(image,bbox,ratio):
    """
    Padding to bbox with ratio

    @image: numpy array of image
    @bbox: the bouding box [x1,y1,x2,y2]
    @ratio: the shorter_size*ratio will be the padding add each side

    @return : the roi after padding
    """
    (H,W)=image.shape[:2]
    #calculate the width and the heigth
    w=bbox[2]-bbox[0]
    h=bbox[3]-bbox[1]

    # the padding will add each side
    d=min(w,h)

    padding_amount=d*ratio

    x1=max(int(bbox[0] - padding_amount),0)
    y1=max(int(bbox[1] - padding_amount),0)
    x2=min(int(bbox[2] + padding_amount),W)
    y2=min(int(bbox[3] + padding_amount),H)

    roi=image[y1:y2,x1:x2]

    return roi

def poly2point(polygon):
    """
    Convert polygon into points (x,y)

    @polygon: the polygon (x1, y1, x2, y2, ...)

    @return: numpy array of points [(x1, y1), (x2, y2), ...]
    """
    points=[]
    for i in range(0,len(polygon),2):
        points.append( (int(polygon[i]), int(polygon[i+1])) )
    return points

def get_orientation_angle_and_center(points): 
    """
    Get the angle and the center to rotate from the polygon

    @points : [ (x1,y1), (x2,y2) ,...] coordinate of polygon

    @return : the angel and the center (x,y) to rotate
    """
    points = np.array(points, dtype=np.float32)
    
    # Calculate the minimum bounding rectangle
    rect = cv2.minAreaRect(points)
    angle = rect[-1]
    center=rect[0]
    
    # Adjust the angle to get the correct orientation
    if angle < -45:
        angle = 90 + angle
    
    return angle, center


def rotate_image(image,center,angle):
    """
    Rotate the image and return the matrix rotation

    @image: array of the image
    @center: (x,y) the center
    @angle : float the angle need to rotate

    @return: the array rotated image and the rotation matrix 
    """
    (h, w) = image.shape[:2]

    angle_rad = math.radians(angle)
    
    # Calculate the new width and height of the image
    new_width = int(abs(w * math.cos(angle_rad)) + abs(h * math.sin(angle_rad)))
    new_height = int(abs(w * math.sin(angle_rad)) + abs(h * math.cos(angle_rad)))


    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale=1.0)

    # Adjust the rotation matrix to take into account the new dimensions
    rotation_matrix[0, 2] += (new_width / 2) - center[0]
    rotation_matrix[1, 2] += (new_height / 2) - center[1]

    rotated_image = cv2.warpAffine(image, rotation_matrix, (new_width, new_height))
    
    return rotated_image,rotation_matrix

    


def deskew_polygon(image,polygon):
    """
    Deskew the polygon and get the rois

    @image: the image contains polygon

    @polygon: the polygon (x1, y1, x2, y2, ...)

    @padding: the padding adding to each size of roi

    @return: list of two rois the deskewed one and the flipped one 
    """
    # get the points from the polygon
    points=poly2point(polygon)

    y_max=max(points, key= lambda point: point[1])[1]
    y_min=min(points, key= lambda point: point[1])[1]

    x1=max([i[0] for i in points if i[1]==y_max])
    x2=max([i[0] for i in points if i[1]==y_min])

    clockwise=x1 > x2

    # get the angle and the center
    angle,center = get_orientation_angle_and_center(points)

    rois=[]

    #if the angle is too small, we dont deskew it
    if abs(angle) > 4 and abs(angle-90) >15 :
        # rotate the image
        if clockwise == False:
            angle=angle-90
        rotated_image,rotation_matrix=rotate_image(image,center,angle)


         # Transform the points
        ones = np.ones(shape=(len(points), 1))
        points_ones = np.hstack([points, ones])
        deskewed_points = rotation_matrix.dot(points_ones.T).T
    else:
        deskewed_points=np.array(points).astype(int)
        rotated_image=image
        angle=0

    #get the roi from the  points of polygon
    x_min=int(min(deskewed_points[:,0]))
    y_min=int(min(deskewed_points[:,1]))
    x_max=int(max(deskewed_points[:,0]))
    y_max=int(max(deskewed_points[:,1]))

    bbox=[x_min, y_min, x_max, y_max]
    #get the roi
    roi=do_padding(rotated_image,bbox,0.05)

    rois.append(roi)

    # this is use for rotate the roi i*90 degree
    # to rotate it until 180 use range(1,4)
    for i in range(2,3):
        # do again with 180
        # rotate the image
        rotated_image,rotation_matrix=rotate_image(image,center,angle+i*90)


         # Transform the points
        ones = np.ones(shape=(len(points), 1))
        points_ones = np.hstack([points, ones])
        deskewed_points = rotation_matrix.dot(points_ones.T).T

    #get the bouding box
        x_min=int(min(deskewed_points[:,0]))
        y_min=int(min(deskewed_points[:,1]))
        x_max=int(max(deskewed_points[:,0]))
        y_max=int(max(deskewed_points[:,1]))

        bbox=[x_min, y_min, x_max, y_max]

        roi=do_padding(image = rotated_image, bbox = bbox, ratio=0.05)
       

        rois.append(roi)

    return rois

# def merge_text(text):
#     result=text[0]["text"]
#     pre_location=text[0]["location"][1]
#     for i in range(1,len(text)):
#         if text[i]["location"][1]-pre_location > 5:
#             result+="\n"
#         else:
#             result+=","
#         result+=text[i]["text"] 
#     return result
def merge_text(text):
    try:
        result=text[0]["text"]
        pre_location=text[0]["location"][1]
        for i in range(len(text)):
            if text[i]["location"][1]-pre_location > 5:
                result+="\n"
            else:
                result+=" "
            result+=text[i]["text"] 
        return result
    except:
        return ""

def extract_text_from_frame(frame_path,text_det,text_recog,threshold_score=0.59):
    filename, ext = os.path.splitext(os.path.basename(frame_path))
    result={}
    all_text=[]
    # save image as array (H,W,C)
    image=cv2.imread(frame_path)
    h=image.shape[0]
    w=image.shape[1]
    image = image[0:int(h*9/10)]

    # detect text and find bounding box
    det_res=text_det(image,progress_bar=False,save_vis=False,out_dir='text_detect_restult')

    #get bounding box
    polygons=det_res['predictions'][0]['polygons']

    # regconize text in each box
    for polygon in polygons:
        #in order to search text easy, we will join all text into an only text
        # To maintain the meaning of all text relatively 
        # this is the basic way
        # if the text A  locates higher than B then in the result : "A B"
        # if A and B both locate as the same height, then prior to the one has x smaller
        # we will use pivot to mark where the text locate
        # pivot is the most left and lowest point in polygon
        pivot=min(poly2point(polygon),key=lambda x: (x[0],x[1]))

        # get the rois after deskewed and padding
        # rois include the roi after deskew and the rotate 180 of it
        rois=deskew_polygon(image=image,polygon=polygon)
        #resize the image height=175, width=400

        text_recog_result=[]

        pass_flag=False
        for roi in rois:
            gray_roi=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
            
            if roi.shape[1]/roi.shape[0]>6 or roi.shape[1]/roi.shape[0] < 2:
                target_size=(400,int(roi.shape[0]*400/roi.shape[1]))
            else:
                target_size=(400,175)
            resize_roi=cv2.resize(gray_roi,target_size,interpolation=cv2.INTER_LINEAR)
            text,score=text_recog.predict(Image.fromarray(resize_roi),return_prob=True)
            text_recog_result.append({"text":text,"score":score})
            if score > 0.699:
                pass_flag=True
                break
        if pass_flag == False:
            text_recog_result.sort(key= lambda x: x["score"])
        the_best_result=text_recog_result[-1]
        #add the location to the text we detect
        the_best_result["location"]=pivot
        if the_best_result["score"] > threshold_score:
            all_text.append(the_best_result)
        else:
            the_best_result["text"]=""
            all_text.append(the_best_result)
    all_text=sorted(all_text,key=lambda x: (x["location"][1],x["location"][0]))
    result[filename]=merge_text(all_text)
    return result

def OCR_from_folder(folder_path,output_dir,threshold_score,det_model_name='textsnake_resnet50-oclip_fpn-unet_1200e_ctw1500',
                                                                    recog_model_name='vgg_seq2seq',):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    #initalize text detection
    text_det=TextDetInferencer(model=det_model_name, device=device)

    # initial text regconition
    config = Cfg.load_config_from_name(recog_model_name)
    config['device']=device
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
                    ocr_result=extract_text_from_frame(frame_path,text_det,text_recog,threshold_score)
                    file_content.update(ocr_result)
        with open(f'{output_dir}/{video_folder}.json','w') as f:
            json.dump(file_content,f,indent=4)