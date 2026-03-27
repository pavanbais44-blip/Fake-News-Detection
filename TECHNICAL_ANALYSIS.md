# 📊 TruthGuard 2.9: Deep Analysis (120% Breakdown)

Here is a 120% technical breakdown of why this project is a sophisticated AI Lab, not just a simple "fake news guesser."

## 🏛️ 1. Multi-Agent Orchestration (The Core)
TruthGuard uses a **decentralized multi-agent architecture**. Instead of one AI doing everything, it separates concerns:
- **ClaimAgent:** Entity extraction and sub-claim decomposition.
- **WebAgent:** High-speed parallel searching using DuckDuckGo News API.
- **ScraperAgent:** Clean text extraction with security hardening.
- **EvidenceAgent:** Semantic similarity comparison (TF-IDF/BERT).
- **BiasAgent:** Sentiment and subjectivity scoring.
- **ReflectionAgent:** Self-correction logic that triggers retries if quality is low.

## 🔬 2. Advanced Forensics (The "Pro" Features)
The system contains specialized modules that go beyond basic NLP:
- **Debate Arena:** An adversarial logic segment where two agents argue the "Pro" and "Con" of a claim.
- **Temporal Module:** Detects "Temporal Drift"—identifying if a news story is misattributed to the wrong time period.
- **Credibility Dictionary:** A library of 25+ high-reputation domains (Reuters, BBC, AP) that act as "Institutional Trust Holders."

## 🧠 3. Experience Engine (The Learning Loop)
TruthGuard doesn't stay the same. It has a **self-learning feedback loop**:
- **SQLite Database:** Every single scan is logged with its truth score and verdict.
- **Human Correction (JSON):** If a user provides feedback, the system stores it and uses it to "boost" the weight of future similar claims.
- **Dynamic Weighting:** The orchestrator adjusts its confidence based on whether it has seen a similar claim before.

## 🔒 4. Security Hardening
Designed for production-grade safety:
- **SSRF Hardening:** Prevents the scraper from accessing internal metadata (like AWS IMDS) or localhost.
- **Forensic Truncation:** Handles long URLs by prioritizing titles and core content to prevent memory blowouts.
- **CORS Hardened:** Strict origin checking to prevent CSRF attacks on the API.

## 🚀 5. Performance Engineering
- **Asynchronous Execution:** Uses Python's `asyncio` and `asyncio.gather` to run web searching, scraping, and bias analysis in parallel, cutting down report time from minutes to seconds.
- **Vite & React 18:** The frontend uses the latest standards for a smooth, high-fidelity user experience.

---
> [!TIP]
> This system is built to be a **Forensic Lab**. It doesn't just give a "Yes/No" but provides a complete trial (search, scrape, debate, decide) for every claim.
