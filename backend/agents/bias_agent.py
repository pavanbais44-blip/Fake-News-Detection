from tools.sentiment_model import sentiment_tool
from typing import Dict, Any

class BiasAgent:
    """Agent responsible for identifying and measuring bias, subjectivity, and tone."""
    
    @staticmethod
    async def analyze(text: str) -> Dict[str, Any]:
        """Detects emotional tone and subjectivity for calculating bias penalties."""
        # 1. BERT Sentiment for tone
        s_res = sentiment_tool.analyze(text[:512])
        sentiment_label = s_res['sentiment']
        subjectivity = s_res['subjectivity']
        
        # 3. Calculate Bias Penalty
        # Penalty should be from 0 to 20 based on the user's constraints
        # Max penalty should be a 0.5 (on a 0-1 scale) if extremely subjective.
        bias_penalty = 0.0
        if subjectivity > 0.7:
             # Normalize bias penalty to be between 0 and 0.5 for the final score reduction
             bias_penalty = round((subjectivity - 0.7) * 1.5, 2)
        
        return {
            "sentiment": sentiment_label,
            "bias_penalty": float(bias_penalty),
            "subjectivity": float(subjectivity),
            "bias_label": "Intense/Subjective" if subjectivity > 0.6 else "Balanced/Factual"
        }
