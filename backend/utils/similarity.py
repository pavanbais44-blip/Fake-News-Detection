from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
import numpy as np

# We used a high-performance vectorizer to simulate deep embeddings 
# in the absence of a dedicated sentence-transformers library.
class SimilarityUtil:
    """Utility for computing semantic embedding similarity between claims and evidence."""
    
    @staticmethod
    def compute(claim: str, doc_list: List[str]) -> List[float]:
        """Calculates semantic similarity using high-dimensional TF-IDF vectors (Upgrade 9)."""
        if not doc_list: return []
        
        # Upgrade 9: Better similarity using n-grams and character-level embeddings
        vectorizer = TfidfVectorizer(
             stop_words='english', 
             ngram_range=(1, 3), 
             analyzer='char_wb' # Captures word sub-patterns / morphology
        )
        
        similarities = []
        for doc in doc_list:
            try:
                tfidf = vectorizer.fit_transform([claim, doc])
                sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
                similarities.append(float(sim))
            except:
                similarities.append(0.0)
                
        return similarities

# Global Instance
similarity_util = SimilarityUtil()
