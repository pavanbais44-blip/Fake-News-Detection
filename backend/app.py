import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from agents.orchestrator import Orchestrator
from tools.scraper import scraper_tool
from collections import defaultdict

app = FastAPI(title="TruthGuard Agentic Core 2.0", description="Upgraded Decentralized AI System for News Analysis")

# 🏛️ CORS SETUP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# 🚦 RATE LIMITER
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

class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

# 🧠 GLOBAL ORCHESTRATOR INSTANCE
orch = Orchestrator()

@app.get("/")
def home():
    return {"status": "TruthGuard Agentic 2.0 Active"}

@app.post("/analyze")
async def analyze_claim(request: AnalyzeRequest):
    """Entry point for the production-grade agentic pipeline."""
    if not request.text and not request.url:
         raise HTTPException(status_code=400, detail="Null input.")
    
    # 🔗 URL to Text Conversion (if needed)
    target_text = request.text
    if request.url and not target_text:
         res = await scraper_tool._extract(request.url)
         target_text = res.get('text', '')
         if not target_text:
              raise HTTPException(status_code=400, detail="Failed to extract text from URL.")

    # 🚀 Start Multi-Agent Search, Scrape & Classification
    try:
        result = await orch.analyze(target_text)
        return result
    except Exception as e:
        print(f"[ERROR] Engine Failure: {e}")
        raise HTTPException(status_code=500, detail=f"Agent System Failure: {str(e)}")

# Legacy compatibility route for original frontend
@app.post("/predict")
async def predict_compatibility(request: AnalyzeRequest):
    # This maps the new agentic result back to the old frontend expected format
    res = await analyze_claim(request)
    
    # Map back to old schema for seamless frontend support
    # We use some data from details to hydrate the response
    return {
        "prediction": res['final_verdict'],
        "status_label": res['final_verdict'].upper(),
        "trust_score": int(res['truth_score'] * 100),
        "message": " | ".join(res['explanation']),
        "related_news": res['details'].get('related_news', []),
        "top_flags": res['explanation'],
        "source_reliability": "Verified" if res['details']['credibility_score'] > 0.5 else "Unknown",
        "domain": "",
        "sentiment": {
            "polarity": 0,
            "subjectivity": res['details'].get('bias_penalty', 0) * 2, # Normalization
            "sentiment_label": "Analyzed",
            "bias_label": "Analyzed"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
