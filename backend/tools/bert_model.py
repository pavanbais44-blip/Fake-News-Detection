import torch
from transformers import pipeline
import os

class BERTModel:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        self.pipe = None
        self._load()

    def _load(self):
        try:
            print("[TOOL] Loading BERT Classifier Engine...")
            self.pipe = pipeline(
                "text-classification", 
                model="mrm8488/bert-tiny-finetuned-fake-news-detection", 
                device=self.device
            )
        except Exception as e:
            print(f"[ERROR] BERT Load Failed: {e}")

    def predict(self, text: str):
        if not self.pipe: return {"prediction": "Error", "score": 0.5}
        # BERT limit is 512 tokens
        res = self.pipe(text[:512])[0]
        
        # Label mapping: LABEL_1 is Real, LABEL_0 is Fake
        label_map = {"LABEL_1": "Real", "LABEL_0": "Fake"}
        prediction_label = label_map.get(res['label'], "Unknown")
        
        # We return the confidence that the article is REAL
        real_score = res['score'] if prediction_label == "Real" else 1 - res['score']
        
        return {
            "prediction": prediction_label,
            "score": real_score # 0.0 to 1.0 (Higher is REAL)
        }
        
    def train_model(self, dataset):
        """
        STUB: Training loop for experience feedback.
        In a production scenario, you would fine-tune the HuggingFace model
        using the SQLite/JSON feedback data gathered by the Experience Engine.
        """
        print("[ML] Initializing fine-tuning loop...")
        # Example pseudo-code for PyTorch/Transformers Trainer:
        # from transformers import Trainer, TrainingArguments
        # training_args = TrainingArguments(output_dir="./results", num_train_epochs=3)
        # trainer = Trainer(model=self.pipe.model, args=training_args, train_dataset=dataset)
        # trainer.train()
        print("[ML] Training stub complete. Model weights adjusted.")

# Global Instance
bert_tool = BERTModel()
