import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, Any, List, Optional

class FeedbackEngine:
    """The 'Experience Engine' that stores and retrieves human corrections to improve future verdicts."""
    
    def __init__(self, db_path: str = "feedback_db.json"):
        self.db_path = db_path
        self.history = self._load_db()

    def _load_db(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as f:
                return json.load(f)
        return []

    def save_correction(self, text: str, label: str):
        """Saves a user's manual correction for a claim."""
        self.history.append({
            "text": text,
            "corrected_label": label,
            "timestamp": str(os.urandom(4).hex()) # simple ID
        })
        with open(self.db_path, "w") as f:
            json.dump(self.history, f, indent=4)
        print(f"[EXPERIENCE] Learned new lesson for: {text[:30]}...")

    def check_experience(self, current_text: str) -> Optional[Dict[str, Any]]:
        """Searches past corrections for similar claims using Cosine Similarity."""
        if not self.history:
            return None
        
        past_texts = [h['text'] for h in self.history]
        vectorizer = TfidfVectorizer().fit(past_texts + [current_text])
        vectors = vectorizer.transform(past_texts + [current_text])
        
        # Compare last vector (current) with all previous
        similarities = cosine_similarity(vectors[-1], vectors[:-1])[0]
        
        if not len(similarities): return None
        
        max_idx = similarities.argmax()
        max_sim = similarities[max_idx]
        
        # Threshold for 'Similar Experience'
        if max_sim > 0.85:
            return {
                "corrected_label": self.history[max_idx]['corrected_label'],
                "similarity": max_sim,
                "reason": "Matching past human correction for a similar claim"
            }
        return None

# Global Instance
feedback_engine = FeedbackEngine()
