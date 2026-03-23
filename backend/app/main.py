import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from app.schema.request import AnalyzeRequest, FinalResult
from app.orchestrator import Orchestrator
from app.agents.scraper_agent import ScraperAgent
from collections import defaultdict

app = FastAPI(title="TruthGuard Agentic API", description="Decentralized multi-agent system for news analysis")

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

# 🧠 GLOBAL ORCHESTRATOR INSTANCE
orch = Orchestrator()

@app.get("/")
def home():
    return {"status": "TruthGuard Agentic Core Active"}

@app.post("/analyze")
async def analyze_claim(request: AnalyzeRequest):
    """Entry point for the agentic analysis pipeline."""
    if not request.text and not request.url:
         raise HTTPException(status_code=400, detail="Null input.")
    
    # Process inputs: if URL, extract text first.
    target_text = request.text
    if request.url and not target_text:
         res = await ScraperAgent._extract_text(request.url)
         target_text = res.get('text', '')
         if not target_text:
              raise HTTPException(status_code=400, detail="Failed to extract text from URL.")

    # 🚀 Start Multi-Agent Pipeline
    try:
        result = await orch.analyze(target_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent System Failure: {str(e)}")

# Legacy compatibility route for original frontend
@app.post("/predict")
async def predict_compatibility(request: AnalyzeRequest):
    # This maps the new agentic result back to the old frontend expected format
    res = await analyze_claim(request)
    
    # Map back to old schema for frontend support
    # We use some data from details to hydrate the response
    return {
        "prediction": res.final_verdict,
        "status_label": res.final_verdict.upper(),
        "trust_score": res.truth_score,
        "message": res.details.get('message', ''),
        "related_news": res.details.get('evidence', {}).get('related_news', []),
        "top_flags": ["BERT-Scan", "Agent-Verified", "Fact-Checked"],
        "source_reliability": "Verified",
        "domain": "",
        "sentiment": {
            "polarity": 0,
            "subjectivity": res.details.get('bias', {}).get('bias_score', 0),
            "sentiment_label": res.details.get('bias', {}).get('sentiment', 'Neutral'),
            "bias_label": res.details.get('bias', {}).get('bias_label', 'Neutral')
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
