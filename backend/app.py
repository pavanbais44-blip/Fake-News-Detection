from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from typing import Optional
from ddgs import DDGS
from newspaper import Article
from textblob import TextBlob
import uvicorn
import re
import os
import joblib
import math
import time
from functools import lru_cache
from urllib.parse import urlparse
from collections import defaultdict

app = FastAPI(title="TruthGuard AI API", description="Hybrid Fact-Checking & Style Analysis")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Rate Limiter
rate_limit_records = defaultdict(list)
@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    rate_limit_records[client_ip] = [t for t in rate_limit_records[client_ip] if now - t < 60]
    if len(rate_limit_records[client_ip]) >= 30:
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")
    rate_limit_records[client_ip].append(now)
    return await call_next(request)

# Global BERT Pipelines (Memory-Efficient Models)
try:
    # Check if GPU is available
    device = 0 if torch.cuda.is_available() else -1
    
    # 🧠 FAKE NEWS BERT: Specialized small transformer for fast classification
    # Using a specialized model: "mrm8488/bert-tiny-finetuned-fake-news-detection"
    detection_pipe = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-fake-news-detection", device=device)
    
    # 😊 SENTIMENT BERT: Highly accurate sentiment analysis
    sentiment_pipe = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=device)
    
    BERT_ACTIVE = True
    print("[SUCCESS] BERT Intelligence Core Active.")
except Exception as e:
    BERT_ACTIVE = False
    print(f"[ERROR] BERT Engine Failure: {e}")

class PredictionRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

def get_related_real_news(query_text: str):
    """Fetches real-time verification evidence from DuckDuckGo."""
    try:
        clean_query = re.sub(r'[^\w\s]', '', query_text[:100])
        # Search for official reports and fact checks
        search_term = f"{clean_query} official news fact"
        with DDGS() as ddgs:
            results = ddgs.text(search_term, max_results=5)
            return [{"title": r.get('title', ''), "url": r.get('href', ''), "body": r.get('body', '')[:200] + "..."} for r in results] if results else []
    except Exception: return []

@lru_cache(maxsize=100)
def extract_text_from_url(url: str):
    try:
        article = Article(url, browser_user_agent='Mozilla/5.0', request_timeout=15)
        article.download()
        article.parse()
        return article.title or "", article.text or ""
    except Exception: return "", ""

@app.get("/")
def read_root():
    return {"status": "BERT Hybrid Engine Active"}

@app.post("/predict")
async def predict_news(request: PredictionRequest):
    if not request.text and not request.url:
        raise HTTPException(status_code=400, detail="Null input.")

    # 🏛️ Domain Reputation Hub
    TRUSTED = {'bbc.com', 'nytimes.com', 'reuters.com', 'apnews.com', 'theguardian.com', 'npr.org'}
    source_reliability, domain = "Unknown", ""
    if request.url:
        domain = urlparse(request.url).netloc.lower().replace('www.', '')
        source_reliability = "Trusted / Verified Source" if domain in TRUSTED else "Unknown Source"

    # Input Collection
    if request.url:
        title, text = await run_in_threadpool(extract_text_from_url, request.url)
        input_data = title + " " + text
        query_text = title if title else input_data
    else:
        input_data = request.text[:50000]
        query_text = request.text[:150]

    # --- 🧠 BERT DEEP LEARNING ANALYSIS ---
    bert_prediction, bert_score = "Fake", 0
    sentiment_label, sentiment_score = "Neutral", 0.5
    top_flags = []

    if BERT_ACTIVE:
        try:
            # 1. Fake News Classification (BERT)
            # The model usually returns labels like 'LABEL_0' (Fake) or 'LABEL_1' (Real)
            # or 'Fake' / 'Real' depending on training. 
            # bert-tiny returns 'LABEL_0' (Fake) and 'LABEL_1' (Real)
            d_res = detection_pipe(input_data[:512])[0] # BERT limit is 512 tokens
            bert_score = int(d_res['score'] * 100)
            
            # Label mapping for mrm8488/bert-tiny
            if d_res['label'] == 'LABEL_1': # Real
                bert_prediction = "Real"
            else: # LABEL_0 is Fake
                bert_prediction = "Fake"
                bert_score = 100 - bert_score # Invert if it's fake confidence

            # 2. Advanced Sentiment (BERT)
            s_res = sentiment_pipe(input_data[:512])[0]
            sentiment_label = s_res['label'].capitalize()
            sentiment_score = s_res['score'] if sentiment_label == "Positive" else 1 - s_res['score']
            
        except Exception as e:
            print(f"BERT Inference Error: {e}")

    # ⚡ HYBRID LAYER: Real-Time Fact Matching
    related = await run_in_threadpool(get_related_real_news, query_text)
    evidence_score_boost = 0
    if related:
        match_keywords = set(word.lower() for word in re.findall(r'\b[a-zA-Z]{5,}\b', query_text))
        best_match_count = 0
        for news in related:
            news_title = news['title'].lower()
            matches = sum(1 for word in match_keywords if word in news_title)
            best_match_count = max(best_match_count, matches)
            # Trusted evidence boost
            news_domain = urlparse(news['url']).netloc.lower().replace('www.', '')
            if any(trusted_d in news_domain for trusted_d in TRUSTED) and matches >= 2:
                evidence_score_boost += 15
        
        if best_match_count >= 3: evidence_score_boost += 30
        elif best_match_count >= 2: evidence_score_boost += 15

    # 🔗 FINAL HYBRID CONCLUSION
    # Final score = BERT Style Score + Evidence Boost
    # If BERT says Real (score high), boost makes it higher.
    # If BERT says Fake (score low), boost pulls it up.
    final_score = bert_score + min(40, evidence_score_boost)
    
    # ⚖️ Subjectivity Penalty (Calculate bias based on sentiment intensity)
    # BERT Sentiment 0.0 or 1.0 means extreme emotion (biased)
    subjectivity = abs(sentiment_score - 0.5) * 2 # 0.0 (neutral) to 1.0 (extremely subjective)
    if subjectivity > 0.7:
        final_score -= int((subjectivity - 0.7) * 40)
        
    final_score = max(5, min(100, final_score))
    final_prediction = "Real" if final_score >= 50 else "Fake"
    
    # Status labeling
    if final_score >= 85: st, msg = "🛡️ VERIFIED TRUTH", "BERT Neural Network confirmed objective patterns & live news records match."
    elif final_score >= 65: st, msg = "✅ LIKELY AUTHENTIC", "High neural alignment with standard reporting; cross-references confirm events."
    elif final_score >= 50: st, msg = "⚖️ PARTIALLY VERIFIED", "Mixed result: neural patterns show bias, but global news events are related."
    elif final_score >= 30: st, msg = "⚠️ SUSPICIOUS", "BERT detected manipulation patterns & lack of verifiable global reports."
    else: st, msg = "🚨 HIGH-RISK", "Strong disinformation patterns detected by Deep Learning. Contradicts global records."

    return {
        "prediction": final_prediction, "status_label": st, "trust_score": final_score, "message": msg,
        "related_news": related, "top_flags": ["Neural-BERT", "Context-Analysis", "Deep-Scan"], # Static flags for BERT
        "source_reliability": source_reliability, "domain": domain,
        "sentiment": {
            "polarity": round(sentiment_score * 2 - 1, 2), # Map to -1 to 1
            "subjectivity": round(subjectivity, 2),
            "sentiment_label": sentiment_label,
            "bias_label": "Intense/Subjective" if subjectivity > 0.6 else "Balanced/Factual"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
