import re
from datetime import datetime
from typing import Dict, Any, List

class TemporalModule:
    """Analyzes news dates and classifies the urgency/risk of misinformation."""
    
    @staticmethod
    def analyze_temporal(text: str) -> Dict[str, Any]:
        """Detects dates (YYYY) and determines if the news is suspiciously old."""
        # Find years like 2018, 2019 etc.
        years = re.findall(r'\b(20\d{2})\b', text)
        years = [int(y) for y in years if 2000 < int(y) < 2026]
        
        current_year = datetime.now().year
        stale_threshold = current_year - 2
        
        is_stale = any(y < stale_threshold for y in years)
        oldest_year = min(years) if years else None
        
        return {
            "contains_dates": bool(years),
            "oldest_detected_year": oldest_year,
            "is_suspiciously_stale": is_stale,
            "temporal_drift": (current_year - oldest_year) if oldest_year else 0
        }

    @staticmethod
    def classify_risk(truth_score: float, patterns: List[str]) -> str:
        """Determines the forensic risk category based on score and found patterns."""
        if truth_score < 0.3:
            return "🔥 CRITICAL MISINFORMATION" if len(patterns) > 1 else "🔴 HIGH RISK"
        elif truth_score < 0.5:
            return "🟡 MEDIUM RISK"
        elif truth_score < 0.7:
            return "🟢 LOW RISK"
        return "✅ VERIFIED/SAFE"

# Global Instance
temporal_module = TemporalModule()
