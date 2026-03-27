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
from database import feedback_engine
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

        # --- 📊 FINAL WEIGHTED SCORING (UPGRADE v2.6) ---
        bert_score = evidence_data['bert_score']
        supporting = evidence_data['supporting']
        contradicting = evidence_data['contradicting']
        cred_score = cred_data['credibility_score']
        bias_penalty = bias_data['bias_penalty']
        
        # --- 📊 NEW WEIGHTED SCORING (Per Prompt Req) ---
        ml_fake_score = evidence_data.get('avg_ml_fake_score', 0.5)
        source_reputation_score = cred_data['credibility_score']
        temporal_drift_score = 1.0 if temporal_res['is_suspiciously_stale'] else 0.0
        bias_score = bias_data['subjectivity']
        
        # Base Weights
        w_ml = 0.5
        w_cred = 0.3
        w_temp = 0.1
        w_bias = 0.1
        
        # 🟢 EXPERIENCE ENGINE WEIGHT ADJUSTMENT
        # If human feedback flagged this before, we trust the ML similarity more.
        if experience:
             w_ml += 0.2
             w_cred -= 0.1
             w_bias -= 0.1

        # Calculate Overall Fake probability
        overall_fake_score = (w_ml * ml_fake_score) + (w_cred * (1 - source_reputation_score)) + (w_temp * temporal_drift_score) + (w_bias * bias_score)
        
        # 🟢 APPLY DIRECT EXPERIENCE BOOST
        # If we have match from a human correction, we shift the result toward it.
        if experience:
             # Higher similarity leads to stronger shift.
             shift = exp_boost * experience['similarity']
             overall_fake_score = max(0.0, min(1.0, overall_fake_score - shift)) # Subtract shift because exp_boost is +0.5 for REAL (lowers fake score)

        
        # 🟢 UPGRADE 16: Strict Evidence Minimum Verification
        # If we found no strong verifiers, the claim is highly likely to be misinformation.
        if supporting == 0:
             overall_fake_score = max(0.75, overall_fake_score + 0.45) # Very Strong shift to Fake
        elif supporting < 2:
             overall_fake_score = max(0.65, overall_fake_score + 0.25) # Moderate shift to Fake
             
        # Direct Contradiction: Sharp penalty for active debunking
        if contradicting > 0:
             overall_fake_score = min(1.0, overall_fake_score + 0.35)
             
        # Normalize strictly to 0.0-1.0
        overall_fake_score = max(0.0, min(1.0, float(overall_fake_score)))
        
        # Convert to Truth Score (1.0 = Real, 0.0 = Fake) for output consistency
        truth_score = 1.0 - overall_fake_score
        
        # Determine Verdict mapping based on Fake probability (Balanced Thresholds)
        final_verdict = "Suspicious"
        if overall_fake_score >= 0.60: final_verdict = "Fake"
        elif overall_fake_score <= 0.35: final_verdict = "Real"
        
        # 🟢 UPGRADE 10: Risk Classification

        risk_level = temporal_module.classify_risk(truth_score, evidence_data['patterns']['patterns_found'])
        
        # 🟢 UPGRADE 6: "What If I'm Wrong?" (Uncertainty Awareness)
        counter_points = []
        if truth_score < 0.5:
             counter_points.append("The system requires at least 2 high-similarity verified sources to mark a claim as REAL.")
             counter_points.append("If this is a developing leak, official reports might not have caught up yet.")
        else:
             counter_points.append("Search results could be biased by search engine algorithms or SEO manipulation.")
             counter_points.append("Verification relies on the integrity of the 'Trusted Source' list.")
        
        # --- 🧪 EXPLAINABILITY REASONS ---
        explanation = []
        if supporting < 2: explanation.append("Insufficient corroborating evidence (less than 2 verified reports found)")
        if contradicting > 0: explanation.append(f"Forensic traces found {contradicting} reports directly debunking this claim")
        if supporting >= 3: explanation.append("Claim is corroborated by multiple independent news organizations")
        if cred_score > 0.7: explanation.append("Sources verifying this data have high institutional trust ratings")
        if bias_penalty > 0.15: explanation.append("Detection of heavy emotional priming and subjective linguistic patterns")
        
        if not explanation:
             explanation.append("Claim analyzed against current news status with moderate confidence")

        # 🟢 UPGRADE: Identify Primary Truth Source (The most relevant 'Real' information)
        truth_source = None
        articles = evidence_data.get('article_results', [])
        if final_verdict == "Fake":
            contradictors = [a for a in articles if a['label'] == "Contradicting"]
            if contradictors:
                truth_source = max(contradictors, key=lambda x: x['similarity'])
        else:
            supporters = [a for a in articles if a['label'] == "Supporting"]
            if supporters:
                truth_source = max(supporters, key=lambda x: x['similarity'])
        
        if not truth_source and articles:
            truth_source = articles[0]

        # --- ✍️ NEURAL SYNTHESIS (Consensus-Based Verdict) ---
        ground_truth = evidence_data.get('ground_truth', 'No clear news consensus found')
        synthesis = f"After scanning {len(scraper_data['evidence_articles'])} channels for relative news, TruthGuard has decided the correct news story is: '{ground_truth}'. "
        
        # Now compare the user prompt to this decided ground truth
        if final_verdict == "Fake":
             synthesis += f"Your prompt DOES NOT match this verified consensus. VERDICT: FAKE. "
        elif final_verdict == "Real":
             synthesis += f"Your prompt matches the verified news cycle. VERDICT: REAL. "
        else:
             synthesis += f"The evidence is inconclusive or the story is too new to verify. VERDICT: SUSPICIOUS. "
             
        if experience:
             synthesis += f"Note: This claim matches a previous verified lesson. "
        
        synthesis += f"We verified this via {supporting} supporting reports from reputable sources. "
        
        if bias_penalty > 0.15:
            synthesis += "The linguistic style is notably subjective, suggesting biased intent. "
        else:
            synthesis += "The language is measured and objective. "
            
        if evidence_data['patterns']['is_clickbait']:
            synthesis += "Warning: Stylistic pattern detection flagged clickbait elements. "
            
        # 🟢 UPGRADE 19: EXPERIENCE HARVESTING
        # Store result for long-term database
        feedback_engine.log_scan(input_text, truth_score, final_verdict, supporting, contradicting)
        
        # 🟢 AUTO-DIDACTIC LEARNING (Self-Training)
        # If the verdict is HIGH CONFIDENCE and has SOLID EVIDENCE, we promote it to an "Experience Lesson"
        # This allows the system to "remember" current news for future similar queries.
        if (supporting >= 3 or contradicting >= 2) and (truth_score > 0.90 or truth_score < 0.10):
             # Only learn if it wasn't already a known experience to avoid redundancy
             if not experience:
                 print(f"[EXPERIENCE] Auto-harvesting high-confidence verdict for: {input_text[:30]}...")
                 feedback_engine.save_correction(input_text, final_verdict)


        return {
            "truth_score": float(truth_score),
            "confidence": reflection_data['confidence'],
            "final_verdict": final_verdict,
            "risk_level": risk_level,
            "explanation": explanation[:3],
            "neural_synthesis": synthesis,
            "truth_source": truth_source,
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
                "ml_fake_impact": round(w_ml * ml_fake_score, 2),
                "reputation_impact": round(w_cred * (1 - source_reputation_score), 2),
                "temporal_impact": round(w_temp * temporal_drift_score, 2),
                "bias_impact": round(w_bias * bias_score, 2),
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
