import torch
from transformers import AutoModel, AutoTokenizer

class VieEmbedding:
    def __init__(self, model_name='bkai-foundation-models/vietnamese-bi-encoder', device='cuda'):
        self.device = torch.device(device)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0] #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def get_embeddings(self, list_text):
        inputs = self.tokenizer(list_text, padding=True, truncation=True, return_tensors="pt", max_length=256).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = self.mean_pooling(outputs, inputs['attention_mask'])

        embeddings = embeddings / torch.norm(embeddings, dim=1, keepdim=True)
        embeddings = embeddings.cpu().numpy()

        return embeddings
    
    def get_embedding(self, text):
        return self.get_embeddings([text])[0]
    
class VieEmbedding_Singleton:
    instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = VieEmbedding(*args, **kwargs)
        return cls.instance