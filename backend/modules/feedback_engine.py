import json
import os
import sqlite3
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, Any, List, Optional

class FeedbackEngine:
    """The 'Experience Engine' that stores and retrieves forensic data to improve future verdicts."""
    
    def __init__(self, db_path: str = "feedback_db.json", history_db: str = "truthguard_experience.db"):
        self.db_path = db_path
        self.history_db = history_db
        self.history = self._load_db()
        self._init_sqlite()

    def _init_sqlite(self):
        """Initializes the long-term forensic experience database."""
        conn = sqlite3.connect(self.history_db)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS scans 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      timestamp TEXT, 
                      claim TEXT, 
                      score REAL, 
                      verdict TEXT, 
                      supporting INTEGER, 
                      contradicting INTEGER)''')
        conn.commit()
        conn.close()

    def log_scan(self, text: str, score: float, verdict: str, supporting: int, contradicting: int):
        """Automated logging of every scan for future ML retraining (Overtime Improvement)."""
        try:
            conn = sqlite3.connect(self.history_db)
            c = conn.cursor()
            c.execute("INSERT INTO scans (timestamp, claim, score, verdict, supporting, contradicting) VALUES (?, ?, ?, ?, ?, ?)",
                      (datetime.now().isoformat(), text[:500], score, verdict, supporting, contradicting))
            conn.commit()
            conn.close()
            print(f"[EXPERIENCE] Logged scan for: {text[:30]}...")
        except Exception as e:
            print(f"[ERROR] Experience Logging Failure: {e}")

    def _load_db(self) -> List[Dict[str, Any]]:
        # Existing JSON feedback loading...
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
        
        # Truncate input to match stored claims (Improvement)
        current_text = current_text[:1000]
        
        past_texts = [h['text'] for h in self.history]
        vectorizer = TfidfVectorizer(
             stop_words='english',
             analyzer='word',
             ngram_range=(1, 2),
             max_features=2500
        )
        
        # Transform both past and current in one step
        vectors = vectorizer.fit_transform(past_texts + [current_text])
        
        # Compare current vector (the last one) with all previous ones
        similarities = cosine_similarity(vectors[-1:], vectors[:-1])[0]
        
        if len(similarities) == 0: return None
        
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
