import asyncio
from typing import List, Dict, Any
from agents.orchestrator import Orchestrator

class EvaluationEngine:
    """Batch evaluation suite for measuring precision, recall, and accuracy (Upgrade 15)."""
    
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator

    async def run_benchmark(self, dataset: List[Dict[str, str]]) -> Dict[str, Any]:
        """Runs the whole pipeline against a labeled dataset."""
        results = []
        correct = 0
        total = len(dataset)
        
        for item in dataset:
            analysis = await self.orchestrator.analyze(item['text'])
            prediction = analysis['final_verdict'] # "Real", "Fake", or "Suspicious"
            actual = item['label'] # "Real" or "Fake"
            
            is_correct = prediction == actual
            if is_correct: correct += 1
            
            results.append({
                "text": item['text'],
                "predicted": prediction,
                "actual": actual,
                "correct": is_correct
            })
            
        return {
            "accuracy": round(correct / total, 2) if total > 0 else 0,
            "total_samples": total,
            "detailed_results": results
        }

evaluation_engine = EvaluationEngine(Orchestrator())
