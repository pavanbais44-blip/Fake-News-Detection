from urllib.parse import urlparse
from typing import List, Dict, Any

class CredibilityModule:
    """Module for measuring the reputation and domain trustworthiness of news evidence."""
    
    TRUSTED_DOMAINS = [
        "bbc.com", "reuters.com", "apnews.com", "ntymes.com", "theguardian.com", 
        "npr.org", "wsj.com", "bloomberg.com", "npr.com", "factcheck.org", "snopes.com"
    ]

    @staticmethod
    def calculate(urls: List[str]) -> Dict[str, Any]:
        """Counts how many articles come from trusted sources and computes a score."""
        trusted_count = 0
        found_trusted = []
        
        for url in urls:
            domain = urlparse(url).netloc.lower().replace('www.', '')
            if any(trusted_d in domain for trusted_d in CredibilityModule.TRUSTED_DOMAINS):
                trusted_count += 1
                found_trusted.append(domain)
        
        # We normalize this score between 0 and 1. 
        # Having at least 2 trusted sources is a solid 100% (1.0)
        cred_score = min(1.0, float(trusted_count / 2.0))
        
        return {
            "credibility_score": cred_score,
            "trusted_count": trusted_count,
            "trusted_domains": list(set(found_trusted))
        }

# Global Instance
credibility_module = CredibilityModule()
