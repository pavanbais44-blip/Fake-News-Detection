import torch
from transformers import pipeline

class SentimentModel:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        self.pipe = None
        self._load()

    def _load(self):
        try:
            print("[TOOL] Loading BERT Sentiment Engine...")
            self.pipe = pipeline(
                "sentiment-analysis", 
                model="distilbert-base-uncased-finetuned-sst-2-english", 
                device=self.device
            )
        except Exception as e:
            print(f"[ERROR] Sentiment Load Failed: {e}")

    def analyze(self, text: str):
        if not self.pipe: return {"sentiment": "Neutral", "score": 0.5, "subjectivity": 0.0}
        # BERT limit is 512 tokens
        res = self.pipe(text[:512])[0]
        
        sentiment_label = res['label'].capitalize()
        
        # Bias Score is mapped 0 (Objective/Balanced) to 1.0 (Extremely Subjective)
        # Higher score means more intense emotion (Biased)
        bias_score = res['score'] if sentiment_label == "Positive" else 1 - res['score']
        subjectivity = abs(bias_score - 0.5) * 2
        
        return {
            "sentiment": sentiment_label,
            "subjectivity": float(subjectivity),
            "bias_score": float(bias_score)
        }

# Global Instance
sentiment_tool = SentimentModel()
