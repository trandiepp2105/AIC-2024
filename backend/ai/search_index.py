from scripts.faiss_search import Faiss_Index
from scripts.embedding_model import CLIP_Embedding
from configs import *

embedding_model = CLIP_Embedding()
index_path = 'faiss_index/index_demo.index'
faiss = Faiss_Index(index_path, embedding_model, load=True)

def image_search(image, top_k=100):
    indexs, distances = faiss.search_image(image, top_k)
    return indexs, distances

def text_search(text, top_k=100):
    indexs, distances = faiss.search_text(text, top_k)
    return indexs, distances