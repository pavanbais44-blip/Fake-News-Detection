import asyncio
from typing import Dict, Any, List
from app.agents.claim_agent import ClaimAgent
from app.agents.web_agent import WebAgent
from app.agents.scraper_agent import ScraperAgent
from app.agents.evidence_agent import EvidenceAgent
from app.agents.bias_agent import BiasAgent
from app.agents.reflection_agent import ReflectionAgent
from app.schema.request import AgentResult, FinalResult

class Orchestrator:
    """The central coordinator that manages the agentic pipeline execution."""
    
    def __init__(self):
        self.max_retries = 1 # Only allowed one retry per requirements

    async def analyze(self, input_text: str, is_url: bool = False) -> FinalResult:
        """Executes the complete multi-agent workflow for analyzing news claims."""
        
        agent_logs: List[AgentResult] = []
        
        # 1. Start with Claim Agent (Extraction)
        claim_data = await ClaimAgent.extract(input_text)
        agent_logs.append(AgentResult(agent_name="ClaimAgent", status="success", data=claim_data))
        
        # 2. Web Agent (Search)
        search_data = await WebAgent.search(keywords=claim_data['keywords'], entities=claim_data['entities'])
        agent_logs.append(AgentResult(agent_name="WebAgent", status="success", data=search_data))
        
        # 3. Scraper Agent (Content Extraction)
        urls = [r['url'] for r in search_data.get('results', [])]
        scraper_data = await ScraperAgent.process_batch(urls)
        agent_logs.append(AgentResult(agent_name="ScraperAgent", status="success", data=scraper_data))
        
        # 4. Evidence Agent (Classification & Support)
        evidence_data = await EvidenceAgent.analyze(input_text, scraper_data['evidence_articles'])
        agent_logs.append(AgentResult(agent_name="EvidenceAgent", status="success", data=evidence_data))
        
        # 5. Bias Agent (Subjectivity)
        bias_data = await BiasAgent.analyze(input_text)
        agent_logs.append(AgentResult(agent_name="BiasAgent", status="success", data=bias_data))
        
        # 6. Reflection Agent (Confidence Check)
        reflection_data = await ReflectionAgent.evaluate(
            bert_score=evidence_data['bert_score'],
            supporting_count=evidence_data['supporting_count'],
            bias_score=bias_data['bias_score']
        )
        agent_logs.append(AgentResult(agent_name="ReflectionAgent", status="success", data=reflection_data))
        
        # --- 🔁 RETRY LOGIC (Step 8 of execution flow) ---
        if reflection_data.get('retry_suggested'):
            print(f"[ORCHESTRATOR] Low confidence detected. Triggering retry with improved query: {reflection_data['suggested_query_addon']}")
            
            # Step 3-5 (Search -> Scrape -> Evidence) repeat with addon
            new_search_data = await WebAgent.search(
                keywords=claim_data['keywords'], 
                entities=claim_data['entities'] + [reflection_data['suggested_query_addon']]
            )
            agent_logs.append(AgentResult(agent_name="WebAgent_Retry", status="success", data=new_search_data))
            
            new_urls = [r['url'] for r in new_search_data.get('results', [])]
            new_scraper_data = await ScraperAgent.process_batch(new_urls)
            agent_logs.append(AgentResult(agent_name="ScraperAgent_Retry", status="success", data=new_scraper_data))
            
            # Re-run Evidence Agent with old + new articles
            all_articles = scraper_data['evidence_articles'] + new_scraper_data['evidence_articles']
            evidence_data = await EvidenceAgent.analyze(input_text, all_articles)
            agent_logs.append(AgentResult(agent_name="EvidenceAgent_Recomputed", status="success", data=evidence_data))
            
            # Re-evaluate confidence
            reflection_data = await ReflectionAgent.evaluate(
                bert_score=evidence_data['bert_score'],
                supporting_count=evidence_data['supporting_count'],
                bias_score=bias_data['bias_score']
            )
            agent_logs.append(AgentResult(agent_name="ReflectionAgent_Verified", status="success", data=reflection_data))

        # --- 📊 FINAL AGGREGATION & SCORING ---
        # Formula: truth_score = (bert_score * 0.7) + (supporting * 0.3) - bias_penalty
        # Map supporting count (max 5 articles) into a 0-100 scale: support_mult = supporting / 5 * 100
        support_val = min(100, (evidence_data['supporting_count'] / 3) * 100) # Scaling for final score
        
        truth_score = (evidence_data['bert_score'] * 0.7) + (support_val * 0.3) - bias_data['bias_penalty']
        truth_score = max(5, min(100, int(truth_score))) # Capping
        
        # Final Verdict Logic
        final_verdict = "Suspicious"
        if truth_score >= 60: final_verdict = "Real"
        elif truth_score < 40: final_verdict = "Fake"
        
        return FinalResult(
            truth_score=truth_score,
            confidence=reflection_data['confidence'],
            final_verdict=final_verdict,
            details={
                "message": f"TruthGuard Agent Network reached a {final_verdict} verdict.",
                "bias": bias_data,
                "evidence": {**evidence_data, "related_news": search_data.get('results', [])},
                "retried": reflection_data.get('retry_suggested', False)
            },
            agent_logs=agent_logs
        )
