import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from agents.orchestrator import Orchestrator
from tools.scraper import scraper_tool
from collections import defaultdict
from fastapi.concurrency import run_in_threadpool

app = FastAPI(title="TruthGuard Agentic Core 2.0", description="Upgraded Decentralized AI System for News Analysis")

# 🏛️ CORS SETUP (HARDENED)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:3000"], 
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# 🛡️ SECURITY HEADERS MIDDLEWARE
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

def validate_url(url: str):
    """Prevents SSRF by blocking internal/loopback IP requests."""
    forbidden = ["localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254"]
    if any(f in url.lower() for f in forbidden):
        raise HTTPException(status_code=400, detail="Security risk: Access to internal metadata/localhost blocked.")

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
    text: Optional[str] = Field(None, max_length=5000)
    url: Optional[str] = Field(None, max_length=500)

# 🧠 GLOBAL ORCHESTRATOR INSTANCE
orch = Orchestrator()

@app.get("/")
def home():
    return {"status": "TruthGuard Agentic 2.0 Active"}

from modules.feedback_engine import feedback_engine
from modules.generator import misinfo_generator
from modules.evaluation import evaluation_engine

class FeedbackRequest(BaseModel):
    text: str = Field(..., max_length=5000)
    label: str

class GenerateRequest(BaseModel):
    text: str = Field(..., max_length=5000)

class EvaluationItem(BaseModel):
    text: str = Field(..., max_length=5000)
    label: str

@app.post("/generate_fake")
async def create_fake(request: GenerateRequest):
    """Generates synthetic misinformation for demo purposes."""
    fake_text = misinfo_generator.generate(request.text)
    return {"original": request.text, "synthetic_fake": fake_text}

@app.post("/evaluate")
async def run_eval(dataset: List[EvaluationItem]):
    """Batch evaluation logic for Upgrade 15."""
    data_list = [{"text": i.text, "label": i.label} for i in dataset]
    res = await evaluation_engine.run_benchmark(data_list)
    return res

@app.post("/feedback")
async def save_feedback(request: FeedbackRequest):
    """Saves human correction to the experience engine."""
    feedback_engine.save_correction(request.text, request.label)
    return {"status": "Success", "message": "Neural Engine has learned from this correction."}

@app.post("/analyze")
async def analyze_claim(request: AnalyzeRequest):
    """Entry point for the production-grade agentic pipeline."""
    if not request.text and not request.url:
         raise HTTPException(status_code=400, detail="Null input.")
    
    # 🔗 URL to Text Conversion (if needed)
    target_text = request.text
    if request.url and not target_text:
         validate_url(request.url)
         try:
             res = await run_in_threadpool(scraper_tool._extract, request.url)
             target_text = res.get('text', '')
             if not target_text:
                  raise HTTPException(status_code=400, detail="Failed to extract text from URL. The page may be protected or empty.")
         except Exception as e:
             raise HTTPException(status_code=500, detail=f"Scraper Error: {str(e)}")

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
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
