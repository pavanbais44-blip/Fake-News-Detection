from typing import Dict, Any, List

class ReflectionAgent:
    """Agent responsible for quality control and retrying low-confidence scans."""
    
    @staticmethod
    async def evaluate(supporting: int, credibility_score: float) -> Dict[str, Any]:
        """Evaluates overall confidence and decides if a search retry is needed."""
        
        # 1. Confidence Evaluation Rules (Step 8 of User Request)
        # If supporting < 2 → LOW confidence
        confidence = "medium"
        action = "finalize"
        
        if supporting < 2:
             confidence = "low"
             action = "retry"
        elif supporting >= 3 and credibility_score > 0.5:
             confidence = "high"
             
        # Suggest improved queries if retry is required
        # Note: Retry logic is only triggered if action is "retry"
        suggested_addon = " news report official fact check"
             
        return {
            "confidence": confidence,
            "action": action,
            "reasoning": f"Confidence is {confidence} based on evidence count {supporting} and credibility {credibility_score}.",
            "suggested_addon": suggested_addon
        }
