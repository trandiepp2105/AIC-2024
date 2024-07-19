from scripts.utils import img_preprocess, create_index_frame
import faiss
import numpy as np

class Faiss_Index:
    def __init__(self,index_path, embedding_model, load=False, embedding_dim=768, id2img=None, _index = faiss.IndexFlatIP):
        self.embedding_model = embedding_model
        self.embedding_dim = embedding_dim
        self.index_path = index_path
        self.index = None
        if not load:
            self.index = create_index_frame(id2img, embedding_model, embedding_dim, _index)
        else:
            print(f'Index loaded from {self.index_path}')
            self.load_index()

    def load_index(self):
        self.index = faiss.read_index(self.index_path)
    
    def save_index(self):
        faiss.write_index(self.index, self.index_path)
    
    def search_text(self, decription, top_k=5):
        text_embedding = self.embedding_model.get_text_embedding(decription).detach().cpu().numpy()
        text_embedding = text_embedding / np.linalg.norm(text_embedding)
        distances, indices = self.index.search(text_embedding, top_k)
        return distances, indices

    def search_image(self, image, top_k=5):
        image_preprocessed = img_preprocess(image)
        image_embedding = self.embedding_model.get_image_embedding(image_preprocessed).detach().cpu().numpy()
        image_embedding = image_embedding / np.linalg.norm(image_embedding)
        distances, indices = self.index.search(image_embedding, top_k)
        return distances, indices

class FaissIndexSingleton:
    _instance = None

    def __new__(cls, index_path, embedding_model, load=True, embedding_dim=768, id2img=None, _index = faiss.IndexFlatIP):
        if cls._instance is None:
            cls._instance = Faiss_Index(index_path, embedding_model, load, embedding_dim, id2img, _index)
        return cls._instance

