import math
import asyncio
from typing import Dict, Any, List
from agents.claim_agent import ClaimAgent
from agents.web_agent import WebAgent
from agents.scraper_agent import ScraperAgent
from agents.evidence_agent import EvidenceAgent
from agents.bias_agent import BiasAgent
from agents.reflection_agent import ReflectionAgent
from modules.credibility import credibility_module
from modules.feedback_engine import feedback_engine
from modules.debate import debate_arena
from modules.temporal import temporal_module

class Orchestrator:
    """The central coordinator that manages the upgraded agentic pipeline execution."""
    
    def __init__(self):
        self.max_retries = 1 

    async def analyze(self, input_text: str) -> Dict[str, Any]:
        """Executes the concurrent multi-agent workflow with parallel processing."""
        
        # 🟢 EXPERIENCE CHECK (Learn from past mistakes)
        experience = feedback_engine.check_experience(input_text)
        exp_boost = 0.0
        if experience:
             print(f"[EXPERIENCE] Matching Past Correction ({experience['corrected_label']}). Experience applied.")
             exp_boost = 0.5 if experience['corrected_label'] == "Real" else -0.5

        # 🟢 PHASE 1: Initial Extraction & Planning
        claim_data = await ClaimAgent.extract(input_text)
        
        # 🟢 PHASE 2: Concurrent Execution
        search_task = WebAgent.get_links(keywords=claim_data['keywords'], entities=claim_data['entities'])
        bias_task = BiasAgent.analyze(input_text)
        
        search_data, bias_data = await asyncio.gather(search_task, bias_task)
        
        # 🟢 PHASE 3: Content Acquisition
        urls = [r['url'] for r in search_data.get('results', [])]
        scraper_data = await ScraperAgent.extract(urls)
        
        # 🟢 PHASE 4: Evidence & Reputation Analysis
        evidence_task = EvidenceAgent.analyze(input_text, scraper_data['evidence_articles'])
        cred_task = asyncio.to_thread(credibility_module.calculate, urls) 
        
        evidence_data, cred_data = await asyncio.gather(evidence_task, cred_task)
        
        # 🟢 PHASE 5: Reflection & Decision
        reflection_data = await ReflectionAgent.evaluate(
            supporting=evidence_data['supporting'],
            credibility_score=cred_data['credibility_score']
        )
        
        # 🟢 PHASE 5: ADVANCED FORENSICS (UPGRADE 1 & 3)
        # Multi-Agent Debate System
        debate_data = debate_arena.run_debate(
             supporting=evidence_data['supporting'], 
             contradicting=evidence_data['contradicting'],
             bert_score=evidence_data['bert_score'],
             patterns=evidence_data['patterns']['patterns_found']
        )
        # Temporal Awareness
        full_text_dump = " ".join([a.get('text', '') for a in scraper_data.get('evidence_articles', [])])
        temporal_res = temporal_module.analyze_temporal(full_text_dump)
        
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
        
        # Calculate components for visual breakdown
        bert_share = (bert_score * 0.6)
        evidence_share = (math.log(1 + supporting) * 0.25)
        cred_share = (cred_score * 0.1)
        neg_bias_share = -(bias_penalty * 0.05)
        
        final_score = bert_share + evidence_share + cred_share + neg_bias_share + exp_boost
        truth_score = max(0.0, min(1.0, float(final_score)))
        
        # Determine Verdict
        final_verdict = "Suspicious"
        if truth_score >= 0.6: final_verdict = "Real"
        elif truth_score < 0.4: final_verdict = "Fake"
        
        # 🟢 UPGRADE 10: Risk Classification
        risk_level = temporal_module.classify_risk(truth_score, evidence_data['patterns']['patterns_found'])
        
        # 🟢 UPGRADE 6: "What If I'm Wrong?" (Uncertainty Awareness)
        counter_points = []
        if truth_score < 0.5:
             counter_points.append("Verdict assumes found news articles accurately describe reality.")
             counter_points.append("If this is a developing situation, older contradictions may be outdated.")
        else:
             counter_points.append("Corroboration might be based on echoing of a single unverified source.")
             counter_points.append("Lack of contradictory evidence does not prove absolute truth.")
        
        # --- 🧪 EXPLAINABILITY REASONS ---
        explanation = []
        if cred_score == 0: explanation.append("No authoritative news sources confirmed this claim")
        if bias_penalty > 0.1: explanation.append("High levels of emotional manipulation detected")
        if supporting < 2: explanation.append("Insufficient corroborating evidence found online")
        if evidence_data['contradicting'] > 1: explanation.append("Multiple reports directly contradict this claim")
        if bert_score < 0.4: explanation.append("Neural patterns align with known disinformation datasets")
        if evidence_data['patterns']['is_clickbait']: explanation.append("Headline uses clickbait stylistic patterns (e.g. ALL CAPS)")
        
        if not explanation:
             explanation.append("Claim is corroborated by trusted sources using neutral reporting styles")

        # --- ✍️ NEURAL SYNTHESIS (Human-Style Conclusion) ---
        synthesis = f"After investigating, TruthGuard has reached a {final_verdict} verdict. "
        if experience:
             synthesis += f"Note: This claim matches a previous human correction (similarity {int(experience['similarity']*100)}%). "
        synthesis += f"We found {supporting} supporting reports from {cred_data['trusted_count']} trusted sources. "
        
        if bias_penalty > 0.15:
            synthesis += "The linguistic style is notably subjective, suggesting biased intent. "
        else:
            synthesis += "The language is measured and objective. "
            
        if evidence_data['patterns']['is_clickbait']:
            synthesis += "Warning: Stylistic pattern detection flagged clickbait elements (e.g. excessive punctuation). "

        return {
            "truth_score": float(truth_score),
            "confidence": reflection_data['confidence'],
            "final_verdict": final_verdict,
            "risk_level": risk_level,
            "explanation": explanation[:3],
            "neural_synthesis": synthesis,
            "debate": debate_data,
            "temporal": temporal_res,
            "counter_points": counter_points,
            "decomposed_claims": claim_data['decomposed_claims'],
            "metadata": {
                "entities": claim_data['entities'],
                "keywords": claim_data['keywords'],
                "patterns": evidence_data['patterns']['patterns_found'],
                "experience_match": bool(experience)
            },
            "score_breakdown": {
                "neural_patterns": round(bert_share, 2),
                "live_evidence": round(evidence_share, 2),
                "credibility_boost": round(cred_share, 2),
                "bias_penalty": round(neg_bias_share, 2),
                "human_correction": round(exp_boost, 2)
            },
            "details": {
                "bert_score": round(bert_score, 2),
                "supporting": supporting,
                "contradicting": evidence_data['contradicting'],
                "credibility_score": round(cred_score, 2),
                "bias_penalty": round(bias_penalty, 2),
                "retried": retried,
                "article_results": evidence_data['article_results'], # GRANULAR DATA FOR UI
                "agent_activities": [
                    {"agent": "ClaimAgent", "task": "Entity Extraction", "status": "Finished"},
                    {"agent": "WebAgent", "task": "Evidence Retrieval", "status": "Finished"},
                    {"agent": "ScraperAgent", "task": "Content Cleaning", "status": "Finished"},
                    {"agent": "EvidenceAgent", "task": "Cross-Comparison", "status": "Finished"},
                    {"agent": "BiasAgent", "task": "Sentiment Processing", "status": "Finished"},
                    {"agent": "ReflectionAgent", "task": "Final Verification", "status": "Finished"}
                ]
            }
        }
