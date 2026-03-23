from tools.scraper import scraper_tool
from typing import Dict, Any, List

class ScraperAgent:
    """Agent responsible for high-speed cleaning and extraction of news text from links."""
    
    @staticmethod
    async def extract(urls: List[str]) -> Dict[str, Any]:
        """Processes links in a batch and cleans output for analysis."""
        # Per requirements, limit results to max 10 articles
        urls = urls[:10]
        
        # 1. Scraping each URL
        articles = await scraper_tool.extract_batch(urls)
        
        return {
            "evidence_count": len(articles),
            "evidence_articles": articles
        }
