from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

class AgentResult(BaseModel):
    agent_name: str
    status: str
    data: Dict[str, Any]
    error: Optional[str] = None

class FinalResult(BaseModel):
    truth_score: float
    confidence: str # low/medium/high
    final_verdict: str # Real/Fake/Suspicious
    details: Dict[str, Any]
    agent_logs: List[AgentResult] = []
