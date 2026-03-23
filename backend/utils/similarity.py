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
             analyzer='char_wb' 
        )
        try:
            # High-performance single-pass vectorization
            tfidf_matrix = vectorizer.fit_transform([claim] + doc_list)
            
            # Compare the first row (the claim) against all other rows (the docs)
            all_sims = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
            return [float(s) for s in all_sims]
        except:
            return [0.0] * len(doc_list)

# Global Instance
similarity_util = SimilarityUtil()
