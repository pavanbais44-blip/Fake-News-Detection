import re
from typing import Dict, Any, List

class ReflectionAgent:
    """Agent responsible for quality control and retrying low-confidence scans."""
    
    @staticmethod
    async def evaluate(bert_score: int, supporting_count: int, bias_score: float) -> Dict[str, Any]:
        """Evaluates overall confidence and decides if a search retry is needed."""
        
        # 1. Base Confidence Calculation
        # High confidence = score > 80 or supporting > 2
        # Low confidence = score between 35-65 and supporting == 0
        confidence = "medium"
        retry_suggested = False
        
        if (bert_score > 80 or bert_score < 20) and supporting_count >= 1:
             confidence = "high"
        elif 35 <= bert_score <= 65 and supporting_count == 0:
             confidence = "low"
             retry_suggested = True
             
        # Suggest improved queries if retry is suggested
        suggested_query_addon = ""
        if retry_suggested:
             suggested_query_addon = " news report fact check"
             
        return {
            "confidence": confidence,
            "retry_suggested": retry_suggested,
            "reasoning": f"Confidence is {confidence} based on bert score {bert_score} and evidence count {supporting_count}.",
            "suggested_query_addon": suggested_query_addon
        }
