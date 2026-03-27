import re
from tools.search import search_tool
from typing import Dict, Any, List

class WebAgent:
    """Agent responsible for multi-query news search and evidence gathering."""
    
    @staticmethod
    async def get_links(keywords: List[str], entities: List[str], retrying: bool = False) -> Dict[str, Any]:
        """Generates 2–3 optimized queries and calls the search tool."""
        
        # 🟢 UPGRADE 11: Context Expansion (Smart Query Expansion)
        # If the input is too vague, expand the context automatically
        working_keywords = list(keywords)
        if len(working_keywords) < 3:
             # Expanding vague claim "India deal" → "India international trade deal news"
             working_keywords.extend(["official report", "fact check", "investigation"])
        
        # 1. Breaking News Query
        breaking_query = " ".join(entities[:3] + working_keywords[:1]) + " breaking news live updates"
        
        # 2. Fact Check Query
        fact_query = " ".join(entities[:2]) + " fact check latest"

        # 3. Regional / Minute-by-minute Context
        live_query = " ".join(entities[:2]) + " news current status right now"
        
        # Add retrying signal if needed
        if retrying:
             breaking_query += " verified official report"
        
        queries = [breaking_query, fact_query, live_query]
        
        # 3. Call Search for each query
        all_results = []
        for q in queries:
             results = search_tool.search_news(q, max_results=5)
             all_results.extend(results)
             
        # Unique links only
        unique_results = {r['url']: r for r in all_results}.values()
        
        return {
            "queries": queries,
            "results": list(unique_results),
            "count": len(unique_results)
        }
