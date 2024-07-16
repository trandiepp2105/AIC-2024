import clip
import torch

class CLIP_Embedding:
    def __init__(self, model_name="ViT-L/14", device="cuda"):
        self.device = device
        self.model, self.preprocess = clip.load(model_name, device=device)

    def get_image_embedding(self, image):
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
        return image_features

    def get_text_embedding(self, text):
        text_input = clip.tokenize(text).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text_input)
        return text_features