import torch
from transformers import pipeline

device = 0 if torch.cuda.is_available() else -1
pipe = pipeline(
    "text-classification", 
    model="mrm8488/bert-tiny-finetuned-fake-news-detection", 
    device=device
)

test_sentences = [
    "The sky is blue and NASA lands on Mars.", # Likely Real
    "Drinking bleach cures cancer according to secret doctors.", # Likely Fake
    "Lionel Messi plays football.", # Likely Real
    "Martians have invaded the White House." # Likely Fake
]

for s in test_sentences:
    res = pipe(s[:512])[0]
    print(f"Sentence: {s}")
    print(f"Prediction: {res['label']} ({res['score']:.4f})")
    print("-" * 20)
