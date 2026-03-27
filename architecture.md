# TruthGuard 2.9 (Consensus Engine) - Architecture Diagram

```mermaid
flowchart TD
    US[User Input: Text or URL] --> |POST /analyze| ORCH[Orchestrator Agent]
    
    subgraph Phase 1: Planning
        ORCH --> CA[Claim Agent]
        CA --> |Decomposes claims & Extracts entities| ORCH
        ORCH --> EXP[(Experience Engine SQLite)]
        EXP -.-> |Historical Match| ORCH
    end

    subgraph Phase 2: Mass Parallel Execution
        ORCH --> WA[Web Agent]
        ORCH --> BA[Bias Agent]
        WA --> |Generates 3+ optimized queries| DDG(DuckDuckGo API)
        DDG --> |Fetches up to 30 raw results| WA
    end

    subgraph Phase 3: Extraction & Cleaning
        WA --> SA[Scraper Agent]
        SA --> |aiohttp proxy rotation| SITES[Live News Sites]
        SITES --> |Raw HTML| SA
        SA --> |newspaper3k clean text| SITES_CLEAN[Cleaned Articles]
    end

    subgraph Phase 4: Forensic Analysis
        SITES_CLEAN --> EA[Evidence Agent]
        ORCH --> EA
        EA --> |TF-IDF Vector Mapping| SIM(Similarity Engine)
        SIM --> |Identifies Consensus / Ground Truth| EA
        EA --> |Checks Contradiction e.g. Death Rumors| EA
        
        SA --> CM[Credibility Module]
        CM --> |Validates domains against 25+ Whitelist| EA
    end

    subgraph Phase 5: Synthesis & Decision
        EA --> ORCH
        BA --> ORCH
        
        ORCH --> DA[Debate Arena]
        DA --> |Alpha (Real) vs Omega (Fake)| DA_JUDGE[Chief Justice]
        DA_JUDGE --> ORCH
        
        ORCH --> TM[Temporal Module]
        TM --> |Checks freshness/urgency| ORCH
    end

    subgraph Phase 6: Verdict
        ORCH --> |Final Scoring Logic| VERDICT{Decision Engine}
        VERDICT --> |Score >= 0.65| REAL[Real]
        VERDICT --> |Score < 0.40| FAKE[Fake]
        VERDICT --> |0.40 - 0.65| SUS[Suspicious]
    end

    REAL --> OUT[Frontend JSON Response]
    FAKE --> OUT
    SUS --> OUT
    
    OUT --> |Feedback| EXP
```
