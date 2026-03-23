from typing import Dict, Any, List

class DebateArena:
    """Simulates a multi-agent debate to provide adversarial reasoning before final verdict."""
    
    @staticmethod
    def run_debate(supporting: int, contradicting: int, bert_score: float, patterns: List[str]) -> Dict[str, Any]:
        """Alpha (Real-Argue) vs Omega (Fake-Argue) - The Disagreement Engine."""
        
        # 🟢 AGENT ALPHA (REAL ARGUMENT)
        real_arg = "The evidence dataset confirms a positive match. "
        if supporting > 1:
            real_arg += f"We found {supporting} independent news sources confirming the details. "
        if bert_score > 0.6:
            real_arg += "Neural patterns align with factual reporting structures."
        else:
            real_arg = "Weak evidence environment, but no explicit markers of fabrication found yet."

        # 🔴 AGENT OMEGA (FAKE ARGUMENT) 
        fake_arg = "Wait! There are significant red flags here. "
        if contradicting > 0:
            fake_arg += f"Detection systems flagged {contradicting} sources as directly contradicting the claim. "
        if patterns:
            fake_arg += f"The linguistic style uses {', '.join(patterns)} - typical of misinformation. "
        if bert_score < 0.4:
            fake_arg += "The neural classification strongly identifies this as a synthetic/manipulated report."
        else:
            fake_arg = "No strong evidence for fake news, but the claim lacks trusted source consensus."

        # ⚖️ CHIEF JUSTICE DECISION
        # Weighted logic for the Judge
        justice_v = "Undetermined"
        if supporting > contradicting and bert_score > 0.5:
            justice_v = "Agent Alpha's corroboration outweighs linguistic suspicions."
        elif contradicting > supporting or bert_score < 0.3:
            justice_v = "Agent Omega's patterns of disinformation are too intense to ignore."
        else:
            justice_v = "Mixed evidence landscape - Caution is advised."

        return {
            "real_argument": real_arg,
            "fake_argument": fake_arg,
            "judge_rationale": justice_v,
            "agents": ["AGENT_ALPHA", "AGENT_OMEGA", "CHIEF_JUSTICE"]
        }

# Global Instance
debate_arena = DebateArena()
