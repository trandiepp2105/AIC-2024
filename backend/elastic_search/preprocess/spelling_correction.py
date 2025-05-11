# Use a pipeline as a high-level helper
from transformers import pipeline

corrector = pipeline("text2text-generation", model="bmd1905/vietnamese-correction-v2")
print("TẢI MÔ HÌNH THÀNH CÔNG!")
MAX_LENGTH = 512

# Define the text samples
texts = [
    "Be na bỏ ra duông",
    "banjn thấy the nà"
]

# Batch prediction
predictions = corrector(texts, max_length=MAX_LENGTH)

# Print predictions
for text, pred in zip(texts, predictions):
    print("- " + pred['generated_text'])