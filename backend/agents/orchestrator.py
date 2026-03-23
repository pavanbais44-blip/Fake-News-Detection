import math
from typing import Dict, Any, List
from agents.claim_agent import ClaimAgent
from agents.web_agent import WebAgent
from agents.scraper_agent import ScraperAgent
from agents.evidence_agent import EvidenceAgent
from agents.bias_agent import BiasAgent
from agents.reflection_agent import ReflectionAgent
from modules.credibility import credibility_module

class Orchestrator:
    """The central coordinator that manages the upgraded agentic pipeline execution."""
    
    def __init__(self):
        self.max_retries = 1 # Only allowed one retry per requirements

    async def analyze(self, input_text: str) -> Dict[str, Any]:
        """Executes the concurrent multi-agent workflow with parallel processing."""
        
        # 🟢 PHASE 1: Initial Extraction & Planning
        # Starts with Claim Agent (This is the primer for everything else)
        claim_data = await ClaimAgent.extract(input_text)
        
        # 🟢 PHASE 2: Concurrent Execution (Speed Optimization)
        # We can search and analyze bias at the same time
        search_task = WebAgent.get_links(keywords=claim_data['keywords'], entities=claim_data['entities'])
        bias_task = BiasAgent.analyze(input_text)
        
        search_data, bias_data = await asyncio.gather(search_task, bias_task)
        
        # 🟢 PHASE 3: Content Acquisition
        urls = [r['url'] for r in search_data.get('results', [])]
        scraper_data = await ScraperAgent.extract(urls)
        
        # 🟢 PHASE 4: Evidence & Reputation Analysis
        # These can also run in parallel
        evidence_task = EvidenceAgent.analyze(input_text, scraper_data['evidence_articles'])
        cred_task = asyncio.to_thread(credibility_module.calculate, urls) # CPU-bound, use thread
        
        evidence_data, cred_data = await asyncio.gather(evidence_task, cred_task)
        
        # 🟢 PHASE 5: Reflection & Decision
        reflection_data = await ReflectionAgent.evaluate(
            supporting=evidence_data['supporting'],
            credibility_score=cred_data['credibility_score']
        )
        
        # --- 🔁 AGENTIC RETRY LOGIC (Self-Correction) ---
        retried = False
        if reflection_data['action'] == "retry":
            print(f"[ORCHESTRATOR] Quality threshold not met. Triggering Neural Retry...")
            retried = True
            new_search_data = await WebAgent.get_links(
                keywords=claim_data['keywords'], 
                entities=claim_data['entities'], 
                retrying=True
            )
            new_urls = [r['url'] for r in new_search_data.get('results', [])]
            new_scraper_data = await ScraperAgent.extract(new_urls)
            
            # Re-run Evidence Agent with old + new articles
            all_articles = scraper_data['evidence_articles'] + new_scraper_data['evidence_articles']
            unique_articles = {a['url']: a for a in all_articles}.values()
            
            evidence_data = await EvidenceAgent.analyze(input_text, list(unique_articles))
            cred_data = credibility_module.calculate(urls + new_urls)
            reflection_data = await ReflectionAgent.evaluate(
                supporting=evidence_data['supporting'],
                credibility_score=cred_data['credibility_score']
            )

        # --- 📊 FINAL WEIGHTED SCORING ---
        bert_score = evidence_data['bert_score']
        supporting = evidence_data['supporting']
        cred_score = cred_data['credibility_score']
        bias_penalty = bias_data['bias_penalty']
        
        final_score = (
            (bert_score * 0.6) + 
            (math.log(1 + supporting) * 0.25) + 
            (cred_score * 0.1) - 
            (bias_penalty * 0.05)
        )
        truth_score = max(0.0, min(1.0, float(final_score)))
        
        # --- 🧪 EXPLAINABILITY REASONS ---
        explanation = []
        if cred_score == 0: explanation.append("No authoritative news sources (Reuters/BBC/etc) confirmed this claim")
        if bias_penalty > 0.1: explanation.append("Neural tone analysis detected high levels of emotional manipulation")
        if supporting < 2: explanation.append("Search agents found insufficient corroborating evidence in the current news cycle")
        if evidence_data['contradicting'] > 1: explanation.append("Multiple reports directly contradict this claim")
        if bert_score < 0.4: explanation.append("Stylistic patterns align with known disinformation datasets")
        
        if not explanation:
             explanation.append("Claim is corroborated by trusted sources using neutral, factual reporting styles")

        # --- ✍️ NEURAL SYNTHESIS (Human-Style Conclusion) ---
        synthesis = f"After scanning {len(urls)} sources, TruthGuard has reached a {final_verdict} verdict. "
        if supporting >= 2:
            synthesis += f"We found {supporting} supporting reports from {cred_data['trusted_count']} trusted domains. "
        else:
            synthesis += f"However, only {supporting} supporting reports were found, indicating an information vacuum. "
        
        if bias_penalty > 0.2:
            synthesis += "The linguistic style is notably subjective, suggesting a non-factual intent. "
        else:
            synthesis += "The language is measured and objective. "
            
        if final_verdict == "Fake":
            synthesis += "Caution: This claim carries significant hallmarks of a coordinated disinformation effort."
        elif final_verdict == "Real":
            synthesis += "The claim appears consistent with verified reporting."

        return {
            "truth_score": float(truth_score),
            "confidence": reflection_data['confidence'],
            "final_verdict": final_verdict,
            "explanation": explanation[:3],
            "neural_synthesis": synthesis,
            "details": {
                "bert_score": round(bert_score, 2),
                "supporting": supporting,
                "contradicting": evidence_data['contradicting'],
                "credibility_score": round(cred_score, 2),
                "bias_penalty": round(bias_penalty, 2),
                "retried": retried,
                "agent_activities": [
                    {"agent": "ClaimAgent", "task": "Entity Extraction", "status": "Finished"},
                    {"agent": "WebAgent", "task": "Evidence Retrieval", "status": "Finished"},
                    {"agent": "ScraperAgent", "task": "Content Cleaning", "status": "Finished"},
                    {"agent": "EvidenceAgent", "task": "Cross-Comparison", "status": "Finished"},
                    {"agent": "BiasAgent", "task": "Sentiment Processing", "status": "Finished"},
                    {"agent": "ReflectionAgent", "task": "Final Verification", "status": "Finished"}
                ],
                "related_news": search_data.get('results', [])
            }
        }
