import re
from tools.search import search_tool
from typing import Dict, Any, List

class WebAgent:
    """Agent responsible for multi-query news search and evidence gathering."""
    
    @staticmethod
    async def get_links(keywords: List[str], entities: List[str], retrying: bool = False) -> Dict[str, Any]:
        """Generates 2–3 optimized queries and calls the search tool."""
        # 1. Base Query from keywords
        base_query = " ".join(entities[:3] + keywords[:2]) + " official news"
        
        # 2. Fact-check Query
        fact_query = " ".join(entities[:2]) + " fact check"

        # 3. Multi-language (Hindi/Regional) Query
        lang_query = " ".join(entities[:2]) + " hindi news report samachar"
        
        # Add retrying signal if needed
        if retrying:
             base_query += " verified source report"
        
        queries = [base_query, fact_query, lang_query]
        
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
