from duckduckgo_search import DDGS
from typing import Dict, Any, List
from functools import lru_cache

class SearchTool:
    """Tool for calling live news search APIs with integrated result caching."""
    
    @staticmethod
    @lru_cache(maxsize=100)
    def search_news(query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Invokes DuckDuckGo for text search results. Cached for performance."""
        # Note: Since the results are lists of dicts (unhashable), 
        # using @lru_cache on staticmethod works for query string.
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=max_results)
                output = [
                    {
                        "title": r.get('title', ''), 
                        "url": r.get('href', ''), 
                        "body": r.get('body', '')[:200] + "..."
                    } for r in results
                ] if results else []
                return output
        except Exception as e:
            print(f"[ERROR] Search Tool Failure: {e}")
            return []

# Global Instance
search_tool = SearchTool()
