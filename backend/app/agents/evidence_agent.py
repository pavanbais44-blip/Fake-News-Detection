import math
import re
from typing import Dict, Any, List
from app.core.models import models

class EvidenceAgent:
    """Agent responsible for cross-referencing and computing the base trust score."""
    
    @staticmethod
    async def analyze(claim_text: str, evidence_articles: List[Dict[str, str]]) -> Dict[str, Any]:
        """Runs the BERT classification on the claim and compares with evidence articles."""
        
        # 1. Base BERT Score (Style Analysis on claim)
        bert_res = models.detection_pipe(claim_text[:512])[0]
        base_score = int(bert_res['score'] * 100)
        
        # Map labels: LABEL_1 is Real, LABEL_0 is Fake
        if bert_res['label'] == 'LABEL_0':
            base_score = 100 - base_score
            base_prediction = "Fake"
        else:
            base_prediction = "Real"
        
        # 2. Support Verification (Evidence Check)
        # Check against existing news articles for matching themes
        supporting_count = 0
        contradicting_count = 0
        
        # Core keywords for matching
        match_keywords = set(word.lower() for word in re.findall(r'\b[a-zA-Z]{5,}\b', claim_text))
        
        for article in evidence_articles:
            # We compare the title and text of the article
            article_content = (article['title'] + " " + article['text']).lower()
            
            # Count keyword matches
            matches = sum(1 for word in match_keywords if word in article_content)
            
            if matches >= 3:
                supporting_count += 1
            elif matches < 1:
                contradicting_count += 1
        
        return {
            "bert_score": base_score,
            "bert_pred": base_prediction,
            "supporting_count": supporting_count,
            "contradicting_count": contradicting_count,
            "evidence_match_confidence": "high" if supporting_count >= 2 else "medium" if supporting_count > 0 else "low"
        }
