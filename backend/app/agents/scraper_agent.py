from newspaper import Article
from typing import Dict, Any, List
from fastapi.concurrency import run_in_threadpool
from functools import lru_cache

class ScraperAgent:
    """Agent responsible for extracting clean text content from URLs."""
    
    @lru_cache(maxsize=100)
    @staticmethod
    def _extract_text(url: str) -> Dict[str, str]:
        """Core sync extraction logic using Newspaper3k."""
        try:
            article = Article(url, browser_user_agent='Mozilla/5.0', request_timeout=15)
            article.download()
            article.parse()
            return {
                "title": article.title or "",
                "text": article.text or "",
                "url": url,
                "status": "success"
            }
        except Exception as e:
            return {
                "title": "",
                "text": "",
                "url": url,
                "status": f"error: {str(e)}"
            }

    @staticmethod
    async def process_batch(urls: List[str]) -> Dict[str, Any]:
        """Processes multiple URLs concurrently using threadpools."""
        # Limit to top 5 evidence urls per requirements
        urls = urls[:5]
        
        results = []
        for url in urls:
            res = await run_in_threadpool(ScraperAgent._extract_text, url)
            if res.get('status') == 'success' and res.get('text'):
                results.append(res)
        
        return {
            "evidence_count": len(results),
            "evidence_articles": results
        }
