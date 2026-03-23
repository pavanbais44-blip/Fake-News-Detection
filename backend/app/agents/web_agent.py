import re
import urllib.parse
from ddgs import DDGS
from typing import Dict, Any, List

class WebAgent:
    """Agent responsible for gathering real-time verification evidence from the web."""
    
    @staticmethod
    async def search(keywords: List[str], entities: List[str] = None) -> Dict[str, Any]:
        """Generates smart search queries and calls DuckDuckGo for evidence."""
        # 1. Generate core search terms: Combine entities and main keywords
        # Only take top 3 entities and top 2 keywords for a clean query
        query_parts = (entities[:3] if entities else []) + (keywords[:2] if keywords else [])
        
        if not query_parts:
            # Fallback query
            query_parts = ["official news fact check"]
        
        search_term = " ".join(query_parts) + " official news"
        
        # 2. Call DuckDuckGo
        try:
            with DDGS() as ddgs:
                results = ddgs.text(search_term, max_results=5)
                formatted = [
                    {
                        "title": r.get('title', ''), 
                        "url": r.get('href', ''), 
                        "body": r.get('body', '')[:200] + "..."
                    } for r in results
                ] if results else []
                
                return {
                    "query": search_term,
                    "results": formatted,
                    "count": len(formatted)
                }
        except Exception as e:
            return {
                "query": search_term,
                "results": [],
                "count": 0,
                "error": str(e)
            }
