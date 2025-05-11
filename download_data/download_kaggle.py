import os
import kaggle as kg
from configs import *

kg.api.authenticate()
# kaggle datasets download -d hkhnhduy/data-v1

output_folder = os.path.join(BASE_FOLDER, 'frames')

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

kg.api.dataset_download_files('hkhnhduy/data-v1', path=output_folder, unzip=True)
os.remove(os.path.join(output_folder, 'data-v1.zip'))