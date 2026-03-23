import os
import torch
from transformers import pipeline
from functools import lru_cache

class ModelManager:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        self.detection_pipe = None
        self.sentiment_pipe = None
        self._initialize_pipelines()

    def _initialize_pipelines(self):
        """Initialize BERT pipelines globally for the agentic backend."""
        try:
            print("[CORE] Initializing BERT Detection Engine...")
            self.detection_pipe = pipeline(
                "text-classification", 
                model="mrm8488/bert-tiny-finetuned-fake-news-detection", 
                device=self.device
            )
            
            print("[CORE] Initializing BERT Sentiment Engine...")
            self.sentiment_pipe = pipeline(
                "sentiment-analysis", 
                model="distilbert-base-uncased-finetuned-sst-2-english", 
                device=self.device
            )
            print("[CORE] Neural Brain Active.")
        except Exception as e:
            print(f"[ERROR] Failed to load Neural Brain: {e}")

# Global instance for shared access across agents
models = ModelManager()
