from scripts.faiss_search import FaissIndexSingleton
from scripts.embedding_model import CLIPSingleton
from configs import *

embedding_model = CLIPSingleton()
index_path = INDEX_FAISS
faiss = FaissIndexSingleton(index_path, embedding_model, load=True)

def image_search(image, top_k=100):
    indexs, distances = faiss.search_image(image, top_k)
    return indexs, distances

def search_text(text, top_k=100):
    distances, indexs = faiss.search_text(text, top_k)
    for i in range(len(indexs[0])):
        indexs[0][i] = int(indexs[0][i])+1
    return indexs, distances