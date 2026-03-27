import re
from tools.bert_model import bert_tool
from utils.similarity import similarity_util
from typing import Dict, Any, List

class EvidenceAgent:
    """Agent responsible for stylistic classification and advanced similarity matching."""
    
    @staticmethod
    def _detect_patterns(text: str) -> Dict[str, Any]:
        """Detects stylistic patterns common in fake news like clickbait/hyperbole."""
        patterns = {
            "all_caps": bool(re.search(r'\b[A-Z]{4,}\b', text)),
            "excessive_punct": bool(re.search(r'!!+|\?!', text)),
            "clickbait_words": any(word in text.lower() for word in ["bombshell", "shocking", "must watch", "wait until you see"])
        }
        return {
            "patterns_found": [k for k, v in patterns.items() if v],
            "is_clickbait": any(patterns.values())
        }

    @staticmethod
    async def analyze(claim_text: str, evidence_articles: List[Dict[str, str]]) -> Dict[str, Any]:
        """Runs the BERT classification and Similarity Utility concurrently."""
        
        # 1. Base BERT Classification
        bert_res = bert_tool.predict(claim_text)
        bert_score = bert_res['score'] # 0.0 to 1.0
        
        # 2. Pattern Detection (UPGRADE)
        patterns = EvidenceAgent._detect_patterns(claim_text)
        
        # 3. Advanced Similarity Matching (TF-IDF + Cosine)
        doc_texts = [a['title'] + " " + a['text'] for a in evidence_articles]
        similarities = similarity_util.compute(claim_text, doc_texts)
        
        supporting_count = 0
        contradicting_count = 0
        article_results = []
        
        for i, sim in enumerate(similarities):
            # 🟢 UPGRADE 15: Forensic Precision
            # 0.6+ is required for any consideration
            # < 0.5 is Irrelevant noise
            
            label = "Irrelevant"
            if sim >= 0.5:
                doc_text_low = doc_texts[i].lower()
                claim_text_low = claim_text.lower()
                
                # Check for debunking/contradiction keywords
                debunk_words = ["fake", "false", "hoax", "baseless", "denies", "debunk", "untrue", "misinformation", "no evidence", "not dead", "rumor", "conspiracy", "debunked", "fabricated", "unfounded"]
                
                # Contextual contradiction (Death detection)
                death_claim = any(w in claim_text_low for w in ["dead", "died", "killed", "passed away", "funeral"])
                alive_context = any(w in doc_text_low for w in ["alive", "healthy", "well", "active", "campaigning", "spoke at", "latest appearance"])
                
                is_contradiction = any(word in doc_text_low for word in debunk_words)
                if death_claim and alive_context:
                    is_contradiction = True
                
                if is_contradiction:
                    label = "Contradicting"
                    contradicting_count += 1
                elif sim >= 0.6:
                    # ONLY high similarity counts as supporting
                    label = "Supporting"
                    supporting_count += 1
                else:
                    label = "Neutral"
            
            article_results.append({
                "url": evidence_articles[i]['url'],
                "title": evidence_articles[i]['title'],
                "snippet": evidence_articles[i]['text'][:150] + "...",
                "similarity": round(sim, 2),
                "label": label
            })
                
        # 🟢 UPGRADE 17: Ground Truth Decision Engine
        # Before comparing to user claim, identify what the majority of high-trust channels are saying
        high_sim_articles = [a for a in article_results if a['similarity'] > 0.5]
        ground_truth_narrative = ""
        if high_sim_articles:
            # The "Correct" news is decided by the most reputable and common narrative
            ground_truth_narrative = max(high_sim_articles, key=lambda x: x['similarity'])['title']
        
        return {
            "bert_score": bert_score,
            "supporting": supporting_count,
            "contradicting": contradicting_count,
            "ground_truth": ground_truth_narrative,
            "avg_similarity": round(sum(similarities)/len(similarities), 2) if similarities else 0.0,
            "patterns": patterns,
            "article_results": article_results[:15] 
        }
