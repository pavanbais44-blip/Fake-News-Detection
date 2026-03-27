import aiohttp
import asyncio
import random
from typing import Dict, Any, List
from functools import lru_cache
from newspaper import Article
from urllib.parse import urlparse

class ScraperAgent:
    """Agent responsible for high-speed cleaning and extraction of news text from links."""
    
    proxies = [
        "http://proxy1.example.com:8080",
        "http://proxy2.example.com:8080",
        "http://proxy3.example.com:8080",
        "http://proxy4.example.com:8080",
        "http://proxy5.example.com:8080"
    ]
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    ]

    @staticmethod
    def _validate_url(url: str):
        """Basic SSRF protection: block internal and local IPs/hostnames."""
        forbidden_hosts = ["localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254"]
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        if not hostname:
            raise ValueError(f"Invalid URL: {url}")
            
        if any(f in hostname.lower() for f in forbidden_hosts):
            raise ValueError("SSRF Risk: Access to internal/local loopback is blocked.")
    
    @staticmethod
    async def _fetch_html(session: aiohttp.ClientSession, url: str) -> str:
        """Asynchronously fetch HTML using a rotated proxy and header."""
        ScraperAgent._validate_url(url)
        
        proxy = random.choice(ScraperAgent.proxies)
        headers = {"User-Agent": random.choice(ScraperAgent.user_agents)}
        
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with session.get(url, headers=headers, timeout=timeout) as response:
                response.raise_for_status()
                return await response.text()
        except Exception as e:
            raise Exception(f"HTTP Fetch Error: {str(e)}")

    @staticmethod
    def _parse_article(html: str, url: str) -> Dict[str, str]:
        """Synchronous parsing of HTML using newspaper3k."""
        try:
             article = Article(url)
             article.set_html(html)
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
    async def _extract_single(url: str) -> Dict[str, str]:
        """Fetch and extract content from a single URL asynchronously."""
        try:
            async with aiohttp.ClientSession() as session:
                html = await ScraperAgent._fetch_html(session, url)
                return ScraperAgent._parse_article(html, url)
        except Exception as e:
            return {
                "title": "",
                "text": "",
                "url": url,
                "status": f"error: {str(e)}"
            }

    @staticmethod
    async def extract(urls: List[str]) -> Dict[str, Any]:
        """Processes links in a batch and cleans output for analysis."""
        urls = urls[:15]
        
        res_list = []
        tasks = [ScraperAgent._extract_single(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for res in results:
             if isinstance(res, dict) and res.get('status') == 'success' and res.get('text'):
                 res_list.append(res)
                 
        return {
            "evidence_count": len(res_list),
            "evidence_articles": res_list
        }
