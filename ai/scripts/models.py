from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import open_clip
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

class CLIP_Embedding:
    def __init__(self, model_name="ViT-L-14", pretrained="commonpool_xl_laion_s13b_b90k", tokenizers='ViT-L-14', device="cuda", use_gpus=False):
        self.device = device
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(model_name, pretrained=pretrained, device=self.device)
        self.model.eval()
        if use_gpus:
            self.model = torch.nn.DataParallel(self.model)
        self.tokenizer = open_clip.get_tokenizer(tokenizers)

    def get_image_embedding(self, image):
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad(), torch.amp.autocast('cuda'):
            image_features = self.model.encode_image(image_input)
        return image_features[0]/image_features[0].norm()
    
    def get_images_embedding(self, images):
        image_input = torch.stack([self.preprocess(image) for image in images]).to(self.device)
        with torch.no_grad(), torch.amp.autocast('cuda'):
            image_features = self.model.encode_image(image_input)
        return image_features/image_features.norm(dim=-1, keepdim=True)

    def get_text_embedding(self, text):
        text_input = self.tokenizer(text).to(self.device)
        with torch.no_grad(), torch.amp.autocast('cuda'):
            text_features = self.model.encode_text(text_input)
        return text_features[0]/text_features[0].norm()
    
    def get_texts_embedding(self, texts):
        text_input = self.tokenizer(texts).to(self.device)
        with torch.no_grad(), torch.amp.autocast('cuda'):
            text_features = self.model.encode_text(text_input)
        return text_features/text_features.norm(dim=-1, keepdim=True)
    
class CLIPSingleton:
    _instance = None
    def __new__(cls, model_name="ViT-L-14", pretrained="commonpool_xl_laion_s13b_b90k", tokenizers='ViT-L-14', device="cuda", use_gpus=False):
        if cls._instance is None:
            cls._instance = CLIP_Embedding(model_name, pretrained, tokenizers, device, use_gpus)
        return cls._instance
    

class Blip_Description:
    def __init__(self, model_name="Salesforce/blip-image-captioning-large", processor_name="Salesforce/blip-image-captioning-large", device="cpu"):
        self.device = torch.device(device)
        self.processor = BlipProcessor.from_pretrained(processor_name, clean_up_tokenization_spaces=True)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

    def generate(self, images):
        inputs = self.processor(images, return_tensors="pt").to(self.device)
        with torch.no_grad(), torch.amp.autocast('cuda'):
            outputs = self.model.generate(**inputs)
        return self.processor.batch_decode(outputs, skip_special_tokens=True)
    
class BlipSingleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = Blip_Description(*args, **kwargs)
        return cls._instance
        