import re
from typing import Dict, Any

class ClaimAgent:
    """Agent responsible for isolating core claims and searchable entities."""
    
    @staticmethod
    async def extract(text: str) -> Dict[str, Any]:
        """Identifies entities and sub-claims for granular decomposition."""
        keywords = list(set(re.findall(r'\b[a-zA-Z]{5,}\b', text)))
        entities = list(set(re.findall(r'\b[A-Z][a-z]+\b', text)))
        
        # 🟢 UPGRADE 2: Claim Decomposition
        # Split into distinct statements for individual verification
        raw_claims = re.split(r'\. | and | but |, ', text)
        decomposed = [c.strip() for c in raw_claims if len(c.strip()) > 15]
        
        return {
            "entities": entities[:10],
            "keywords": keywords[:15],
            "text_length": len(text),
            "decomposed_claims": [{"id": i, "text": c} for i, c in enumerate(decomposed[:3])]
        }
