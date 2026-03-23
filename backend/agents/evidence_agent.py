from tools.bert_model import bert_tool
from utils.similarity import similarity_util
from typing import Dict, Any, List

class EvidenceAgent:
    """Agent responsible for stylistic classification and advanced similarity matching."""
    
    @staticmethod
    async def analyze(claim_text: str, evidence_articles: List[Dict[str, str]]) -> Dict[str, Any]:
        """Runs the BERT classification and Similarity Utility concurrently."""
        
        # 1. Base BERT CLassification
        bert_res = bert_tool.predict(claim_text)
        bert_score = bert_res['score'] # 0.0 to 1.0
        
        # 2. Advanced Similarity Matching (TF-IDF + Cosine)
        doc_texts = [a['title'] + " " + a['text'] for a in evidence_articles]
        similarities = similarity_util.compute(claim_text, doc_texts)
        
        # Classify articles based on user thresholds:
        # > 0.5 = Supporting, < 0.2 = Contradicting
        supporting_count = 0
        contradicting_count = 0
        matching_scores = []
        
        for sim in similarities:
            matching_scores.append(round(sim, 2))
            if sim >= 0.5:
                supporting_count += 1
            elif sim <= 0.2:
                contradicting_count += 1
                
        return {
            "bert_score": bert_score,
            "supporting": supporting_count,
            "contradicting": contradicting_count,
            "avg_similarity": round(sum(similarities)/len(similarities), 2) if similarities else 0.0,
            "all_sim_scores": matching_scores
        }
