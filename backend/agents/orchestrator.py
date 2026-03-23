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
        """Executes the complete multi-agent workflow for analyzing news claims."""
        
        # 1. Claim Agent (Extraction)
        claim_data = await ClaimAgent.extract(input_text)
        
        # 2. Web Agent (First Search)
        search_data = await WebAgent.get_links(keywords=claim_data['keywords'], entities=claim_data['entities'])
        
        # 3. Scraper Agent (Extract Text)
        urls = [r['url'] for r in search_data.get('results', [])]
        scraper_data = await ScraperAgent.extract(urls)
        
        # 4. Evidence Agent (BERT + Similarity)
        evidence_data = await EvidenceAgent.analyze(input_text, scraper_data['evidence_articles'])
        
        # 5. Bias Agent (Tone Analysis)
        bias_data = await BiasAgent.analyze(input_text)
        
        # 6. Credibility Module (Domain Reputation)
        cred_data = credibility_module.calculate(urls)
        
        # 7. Reflection Agent (Confidence Check)
        reflection_data = await ReflectionAgent.evaluate(
            supporting=evidence_data['supporting'],
            credibility_score=cred_data['credibility_score']
        )
        
        # --- 🔁 AGENTIC RETRY LOGIC (Step 8 of User Request) ---
        if reflection_data['action'] == "retry":
            print(f"[ORCHESTRATOR] Low confidence detected. Retrying once with improved queries...")
            new_search_data = await WebAgent.get_links(
                keywords=claim_data['keywords'], 
                entities=claim_data['entities'], 
                retrying=True
            )
            new_urls = [r['url'] for r in new_search_data.get('results', [])]
            new_scraper_data = await ScraperAgent.extract(new_urls)
            
            # Re-run Evidence Agent with old + new articles
            all_articles = scraper_data['evidence_articles'] + new_scraper_data['evidence_articles']
            # Dedup by title
            unique_articles = {a['title']: a for a in all_articles}.values()
            
            evidence_data = await EvidenceAgent.analyze(input_text, list(unique_articles))
            # Re-calculate credibility with new URLs
            cred_data = credibility_module.calculate(urls + new_urls)
            # Final reflection
            reflection_data = await ReflectionAgent.evaluate(
                supporting=evidence_data['supporting'],
                credibility_score=cred_data['credibility_score']
            )

        # --- 📊 UPGRADED SCORING SYSTEM (Step 6 of User Request) ---
        # Formula: score = (bert_score * 0.6 + log(1 + supporting) * 0.25 + credibility_score * 0.1 - bias_penalty * 0.05)
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
        # Normalize between 0 and 1
        truth_score = max(0.0, min(1.0, float(final_score)))
        
        # --- 🧪 EXPLAINABILITY (Step 11 of User Request) ---
        explanation = []
        if cred_score == 0: explanation.append("No trusted sources found")
        if bias_penalty > 0.1: explanation.append("High emotional bias detected")
        if supporting < 2: explanation.append("Low supporting evidence")
        if evidence_data['contradicting'] > 0: explanation.append("Contradicting reports present")
        if bert_score < 0.4: explanation.append("Neural model flagged stylistic manipulation")
        
        if not explanation:
             explanation.append("Claim is supported by objective reporting and stylistic patterns")

        # Determine Final Verdict
        final_verdict = "Suspicious"
        if truth_score >= 0.6: final_verdict = "Real"
        elif truth_score < 0.4: final_verdict = "Fake"
        
        return {
            "truth_score": float(truth_score),
            "confidence": reflection_data['confidence'],
            "final_verdict": final_verdict,
            "explanation": explanation[:3], # Return top 3 reasons
            "details": {
                "bert_score": round(bert_score, 2),
                "supporting": supporting,
                "contradicting": evidence_data['contradicting'],
                "credibility_score": round(cred_score, 2),
                "bias_penalty": round(bias_penalty, 2),
                "retried": (reflection_data['action'] == "finalize" and "retrying" in str(reflection_data)), # Rough flag
                "related_news": search_data.get('results', [])
            }
        }
