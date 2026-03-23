import re
from typing import Dict, Any

class ClaimAgent:
    """Agent responsible for identifying and extracting core claims of news."""
    
    @staticmethod
    async def extract(text: str) -> Dict[str, Any]:
        """Exxtracts core nouns and keywords using regex for speed and efficiency."""
        # Simple extraction logic for keywords (words > 5 chars)
        # In a real production system, this could use spaCy for Entity Recognition.
        # But per constraints, we keep existing logic fast.
        keywords = list(set(re.findall(r'\b[a-zA-Z]{5,}\b', text)))
        
        # Simple entity simulation: find capitalized words that aren't at start of sentence
        potential_entities = list(set(re.findall(r'\b[A-Z][a-z]+\b', text)))
        
        return {
            "entities": potential_entities[:10],
            "keywords": keywords[:15],
            "text_length": len(text)
        }
