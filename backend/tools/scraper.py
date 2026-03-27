from newspaper import Article
from functools import lru_cache
from typing import Dict, Any, List
from fastapi.concurrency import run_in_threadpool

class ScraperTool:
    """Tool for clean extraction of news content from URLs."""
    
    @staticmethod
    @lru_cache(maxsize=150)
    def _extract(url: str) -> Dict[str, str]:
        """Synchronous core extraction."""
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
    async def extract_batch(urls: List[str]) -> List[Dict[str, str]]:
        """Wraps sync extraction in threadpool for async batch processing."""
        res_list = []
        for url in urls:
            res = await run_in_threadpool(ScraperTool._extract, url)
            if res.get('status') == 'success' and res.get('text'):
                res_list.append(res)
        return res_list

# Global Instance
scraper_tool = ScraperTool()
