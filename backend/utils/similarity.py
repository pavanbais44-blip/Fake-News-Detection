from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

class SimilarityUtil:
    """Utility for computing textual similarity between claims and evidence."""
    
    @staticmethod
    def compute(claim: str, doc_list: List[str]) -> List[float]:
        """Calculates cosine similarity of the claim against a list of documents."""
        if not doc_list: return []
        
        vectorizer = TfidfVectorizer(stop_words='english')
        
        # We compute similarity for each document individually to the claim
        # First entry is always the claim
        similarities = []
        for doc in doc_list:
            # Simple TF-IDF comparison
            tfidf = vectorizer.fit_transform([claim, doc])
            sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
            similarities.append(float(sim))
            
        return similarities

# Global Instance
similarity_util = SimilarityUtil()
