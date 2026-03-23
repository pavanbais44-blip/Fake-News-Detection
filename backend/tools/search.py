from ddgs import DDGS
from typing import Dict, Any, List

class SearchTool:
    """Tool for calling live news search APIs."""
    
    @staticmethod
    def search_news(query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Invokes DuckDuckGo for text search results."""
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=max_results)
                return [
                    {
                        "title": r.get('title', ''), 
                        "url": r.get('href', ''), 
                        "body": r.get('body', '')[:200] + "..."
                    } for r in results
                ] if results else []
        except Exception as e:
            print(f"[ERROR] Search Tool Failure: {e}")
            return []

# Global Instance
search_tool = SearchTool()
