from typing import Dict, Any
from app.core.models import models

class BiasAgent:
    """Agent responsible for identifying and measuring bias and subjectivity."""
    
    @staticmethod
    async def analyze(text: str) -> Dict[str, Any]:
        """Detects emotional tone and subjectivity for calculating penalties."""
        # 1. BERT Sentiment for tone
        s_res = models.sentiment_pipe(text[:512])[0]
        sentiment_label = s_res['label'].capitalize()
        
        # 2. Subjectivity (Bias) based on sentiment intensity
        # Bias Score is mapped 0 (Objective) to 1.0 (Extremely Subjective)
        bias_score = s_res['score'] if sentiment_label == "Positive" else 1 - s_res['score']
        subjectivity = abs(bias_score - 0.5) * 2
        
        # 3. Calculate Bias Penalty: Higher subjectivity leads to a higher penalty
        # Penalty should be around 0 to 25 based on the user's constraints
        bias_penalty = 0
        if subjectivity > 0.7:
             bias_penalty = int((subjectivity - 0.7) * 50)
        
        return {
            "bias_score": round(subjectivity, 2),
            "sentiment": sentiment_label,
            "bias_penalty": bias_penalty,
            "bias_label": "Intense/Subjective" if subjectivity > 0.6 else "Balanced/Factual"
        }
