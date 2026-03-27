# 🛡️ TruthGuard 2.9: Multi-Agent Forensic Laboratory

TruthGuard is a state-of-the-art **Agentic AI** system designed for real-time fake news detection and misinformation forensics. Unlike traditional static models, TruthGuard 2.9 uses a **Consensus Engine** that scans live global news cycles and aggregates evidence from multiple independent channels to reach a verdict.

---

## 🏛️ System Architecture: The Multi-Agent Pipeline

TruthGuard operates on a decentralized agentic workflow where specialized AI agents collaborate to verify a claim.

### 1. 🧠 Orchestrator Agent (The Brain)
The central coordinator that manages parallel execution, weighted scoring, and final verdict synthesis.
- **Strict Evidence Minimum:** Requires at least 2 high-similarity reputable sources to mark a claim as "REAL."
- **Institutional Trust Multiplier:** Amplifies evidence weight if it originates from high-repute global news domains.
- **Neural Synthesis:** Generates a human-style forensic conclusion explaining the "Ground Truth."

### 2. 🔍 Claim Agent (Decomposition)
- **Granular Analysis:** Breaks down long user prompts into distinct, searchable sub-claims.
- **Entity Extraction:** Identifies key people, organizations, and locations involved.

### 3. 🌐 Web Agent (Mass Search)
- **Channel Expansion:** Generates and executes 3+ optimized search queries simultaneously.
- **Massive Scan:** Retrieval of up to **30 independent news results** (DuckDuckGo News Index).

### 4. 🧹 Scraper Agent (Extraction)
- **High-Speed Cleaning:** Extracts clean text and metadata from up to **15 top-tier results** concurrently.
- **SSRF Hardened:** Built-in protection against scanning restricted or internal loopback IPs.

### 5. 🔬 Evidence Agent (Cross-Comparison)
- **Semantic Mapping:** Uses high-dimensional TF-IDF vectors for semantic similarity.
- **Contextual Contradiction:** Specifically tuned to detect "Death Rumors" (checking for 'alive' context vs 'dead' claims).
- **Consensus Decision:** Decides the "Official Story" by finding the majority narrative among channels.

---

## 🎭 Specialized Forensic Modules

*   **Alpha vs Omega Debate:** An adversarial reasoning module where two agents argue the "Real" and "Fake" sides of a claim before a "Judge" (Orchestrator) decides.
*   **Credibility Module:** A library of **25+ reputable news domains** (Reuters, BBC, AP, TOI, etc.) used to verify source integrity.
*   **Experience Engine (Feedback):** A self-learning loop that stores every scan in a **SQLite Forensic Database** and learns from human corrections via a JSON database.
*   **Temporal Module:** Detects "Temporal Drift" to identify if news is suspiciously old or misattributed.
*   **Bias Agent:** Measures emotional priming, subjectivity, and sentiment-based linguistic manipulation.

---

## 🚀 Installation & Launch

### 🐍 Backend (Agentic Engine)
Requires Python 3.13+ and `uv` package manager.
```bash
cd backend
uv sync
uv run python app.py
```
*Port: 8000*

### ⚛️ Frontend (Research Dashboard)
Requires Node.js and `npm`.
```bash
cd frontend
npm install
npm run dev
```
*Port: 5173*

---

## 🔒 Security & Performance
- **Forensic Truncation:** Stabilized to handle long URL analysis without memory blowouts.
- **SSRF Protection:** Blocks access to internal metadata and localhost.
- **Hardened CORS:** Only allows verified frontend origins to prevent unauthorized API access.
- **Fault-Tolerant I/O:** Isolated database logging ensures the system stays online even during disk/lock issues.

---

## 📄 API Reference

### `POST /analyze`
The primary entry point for the agentic laboratory.
- **Request:** `{"text": "Claim here"}` or `{"url": "Link here"}`
- **Response:**
    - `truth_score`: 0.0 to 1.0 (float)
    - `final_verdict`: "Real", "Fake", "Suspicious"
    - `neural_synthesis`: Detailed human-style explanation
    - `truth_source`: The most relevant article link found

---
*TruthGuard 2.9 (Consensus Engine) - Advanced Forensic Misinformation Analysis.*
