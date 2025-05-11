import torch
import torch.amp
import open_clip
from transformers import CLIPTokenizer, CLIPTextModelWithProjection

class CLIP_Embedding:
    def __init__(self, model_name="ViT-L-14", pretrained="commonpool_xl_laion_s13b_b90k", device="cuda", tokenizers = 'ViT-L-14'):
        self.device = device
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(model_name, pretrained=pretrained, device=self.device)
        self.tokenizer = open_clip.get_tokenizer(tokenizers)

    def get_image_embedding(self, image):
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad(), torch.amp.autocast('cuda'):
            image_features = self.model.encode_image(image_input)
        return image_features[0]/image_features[0].norm()

    def get_text_embedding(self, text):
        text_input = self.tokenizer(text).to(self.device)
        with torch.no_grad(), torch.amp.autocast('cuda'):
            text_features = self.model.encode_text(text_input)
        return text_features[0]/text_features[0].norm()
    
class CLIPSingleton:
    _instance = None
    def __new__(cls, model_name="ViT-L-14", pretrained="commonpool_xl_laion_s13b_b90k", device="cuda", tokenizers='ViT-L-14'):
        if cls._instance is None:
            cls._instance = CLIP_Embedding(model_name, pretrained, device, tokenizers)
        return cls._instance
    
class CLIP4CLIP_Embedding:
    def __init__(self, pretrain = 'Searchium-ai/clip4clip-webvid150k', device = 'cuda'):
        self.device = device
        self.model = CLIPTextModelWithProjection.from_pretrained(pretrain).to(device)
        self.tokenizer = CLIPTokenizer.from_pretrained(pretrain)

    def embedding_text(self, search_text):
        inputs = self.tokenizer(text=search_text , return_tensors="pt").to(self.device)
        outputs = self.model(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"])

        final_output = outputs[0] / outputs[0].norm(dim=-1, keepdim=True)
        final_output = final_output.cpu().detach().numpy()
        return final_output[0]
            
class CLIP4CLIPSingleton:
    _instance = None
    def __new__(cls, pretrain = 'Searchium-ai/clip4clip-webvid150k', device = 'cuda'):
        if cls._instance is None:
            cls._instance = CLIP4CLIP_Embedding(pretrain, device)
        return cls._instance
