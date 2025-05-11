# Extract keyframes
FRAME_WIDTH=640
FRAME_HEIGHT=480
THRESHOLD_SIMILARITY=0.8

KEYFRAME_PROCESS=3

MODELS_CLIP_NAME='ViT-B-32'
PRETRAINED_CLIP='datacomp_xl_s13b_b90k'
TOKENIZER_CLIP='ViT-B-32'

BATCH_CLIP_SIZE=128

#Description embedding
DE_MODEL="Salesforce/blip-image-captioning-base"
DE_PROCESSOR="Salesforce/blip-image-captioning-base"
DE_BATCH_SIZE=128
DE_EMBEDDING_BATCH_SIZE=128


#Object detection
MODEL_YOLOV8='yolov8s.pt'
BATCH_SIZE_YOLO=64
MODEL_YOLO_ROOT='/data/models'

#OCR
THRESHOLD_SCORE=0.59
OCR_EMBEDDING_BATCH=512

#Database
MAX_NEXTFRAME=5
NUM_PROCESSES_DB=4
NUM_PROCESSES_NEXTFRAME=4

KEYFRAME_VOLUME_DIR='/data/keyframes'
EMBEDDING_VOLUME_DIR='/data/embeddings'
OBJECTS_VOLUME_DIR='/data/objects'
VIDEOS_VOLUME_DIR='/data/videos'
FRAMES_VOLUME_DIR='/data/frames'
OCR_VOLUME_DIR='/data/ocrs'
DE_VOLIME_DIR='/data/descriptions'
DE_EMBEDDING_VOLUME_DIR='/data/description_embeddings'
KF_CSV_VOLUME_DIR='/data/csv'
OCR_EMBEDDING_VOLUME_DIR='/data/ocr_embeddings'
DATABASE_VOLUME_DIR='/data/database'
DATABASE_NEXTFRAME_VOLUME_DIR='/data/database_nextframe'
MODELS_VOLUME_DIR='/models'

EMBEDDING_V2 = '/data/embeddings_v2'

# #Super config

# # Extract keyframes
# FRAME_WIDTH=640
# FRAME_HEIGHT=480
# THRESHOLD_SIMILARITY=0.9

# KEYFRAME_PROCESS=8

# MODELS_CLIP_NAME='ViT-H-14-378-quickgelu'
# PRETRAINED_CLIP='dfn5b'
# TOKENIZER_CLIP='ViT-H-14-378-quickgelu'

# BATCH_CLIP_SIZE=300

# #Description embedding
# DE_MODEL="Salesforce/blip-image-captioning-base"
# DE_PROCESSOR="Salesforce/blip-image-captioning-base"
# DE_BATCH_SIZE=512
# DE_EMBEDDING_BATCH_SIZE=512


# #Object detection
# MODEL_YOLOV8='yolov8m.pt'  # n / s / m / l / x
# BATCH_SIZE_YOLO=124
# MODEL_YOLO_ROOT='/data/models_yolo'


# #OCR
# THRESHOLD_SCORE=0.59
# OCR_EMBEDDING_BATCH=512

# #Database
# MAX_NEXTFRAME=5
# NUM_PROCESSES_DB=12
# NUM_PROCESSES_NEXTFRAME=12

# KEYFRAME_VOLUME_DIR='/data/keyframes'
# EMBEDDING_VOLUME_DIR='/data/embeddings'
# OBJECTS_VOLUME_DIR='/data/objects'
# VIDEOS_VOLUME_DIR='/data/videos/video'
# FRAMES_VOLUME_DIR='/data/frames'
# OCR_VOLUME_DIR='/data/ocrs'
# DE_VOLIME_DIR='/data/descriptions'
# DE_EMBEDDING_VOLUME_DIR='/data/description_embeddings'
# KF_CSV_VOLUME_DIR='/data/keyframes_csv'
# OCR_EMBEDDING_VOLUME_DIR='/data/ocr_embeddings'
# DATABASE_VOLUME_DIR='/data/database'
# DATABASE_NEXTFRAME_VOLUME_DIR='/data/database_nextframe'
# MODELS_VOLUME_DIR='/models'



