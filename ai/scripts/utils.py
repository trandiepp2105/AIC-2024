from PIL import Image
from torchvision import transforms
import faiss
from tqdm import tqdm
import numpy as np

def img_preprocess(img_path, transform=transforms.Compose([transforms.Resize((1024, 1024))]), expand_dims=False):
    img = Image.open(img_path)
    img = transform(img)
    if expand_dims:
        img = img.unsqueeze(0)
    return img

def path2Embedding(img_path, embedding_model):
    img = img_preprocess(img_path)
    img_embedding = embedding_model.get_image_embedding(img).detach().numpy()
    return img_embedding

def create_index_frame(id2img, embedding_model, embedding_dim=768, _index = faiss.IndexFlatIP):
    frame_index = _index(embedding_dim)
    for img_id, img_path in tqdm(id2img.items()):
        try:
            img = img_preprocess(img_path)
            img_embedding = embedding_model.get_image_embedding(img).detach().cpu().numpy()
            img_embedding = img_embedding / np.linalg.norm(img_embedding) # Normalize
            frame_index.add(img_embedding)
        except Exception as e:
            print(f"Error processing image {img_path}: {e}")
    return frame_index