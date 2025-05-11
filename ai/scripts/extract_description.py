from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

class Blip_Description:
    def __init__(self, model_name="Salesforce/blip-image-captioning-base", processor_name="Salesforce/blip-image-captioning-base", device="cpu"):
        self.device = torch.device(device)
        self.processor = BlipProcessor.from_pretrained(processor_name)
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
        