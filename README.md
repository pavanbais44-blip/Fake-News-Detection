# 🛡️ TruthGuard 2.5: Agentic Real-Time Misinformation Forensics Lab

![TruthGuard Banner](https://img.shields.io/badge/Status-Hardened--Production-brightgreen) ![License](https://img.shields.io/badge/License-MIT-green) ![Engine](https://img.shields.io/badge/Architecture-Multi--Agent_System-blueviolet) ![Performance](https://img.shields.io/badge/Speed-Optimized_via_uv-orange)

## 📌 Project Overview
TruthGuard 2.5 is a decentralized, **Multi-Agent Forensic Laboratory** designed for the professional-grade detection and analysis of digital disinformation. Unlike standard AI classifiers, TruthGuard 2.5 doesn't just "guess"; it **investigates the live truth** in real-time.

The system employs a team of specialized AI agents that collaborate, debate, and cross-reference **minute-by-minute global news** to reach a high-fidelity "Neural Verdict." Version 2.5 introduces **Live News Indexing**, **SSRF-Hardened Security**, and an automated **Fact-Check Correction Engine**.

---

## 🧠 Phase 3: Agentic Architecture (The Intelligence Hub)

TruthGuard 2.0 utilizes a **Decentralized Multi-Agent Workflow** where each component has a specific forensic task:

### 🎭 1. Neural Debate Arena (`ALPHA` vs `OMEGA`)
The final verdict is reached through an adversarial cross-examination. **Agent ALPHA** argues for the "Real" case, while **Agent OMEGA** focuses on finding disinformation patterns. A **Chief Justice Agent** then weighs the conflicting arguments to provide a transparent, critical-thinking rationale.

### 🧊 2. Atomic Claim Decomposition
Instead of analyzing a broad paragraph, the `ClaimAgent` breaks complex text into **atomic sub-claims**. Each claim is verified individually against global news databases, ensuring that partial truths don't hide bigger lies.

### 🕰️ 3. Temporal Awareness & Staleness Detection
Fake news often uses real footage or articles from years ago and presents them as "Breaking News." Our `TemporalModule` detects date-stamps in evidence and flags news older than 2 years as **"Suspiciously Stale."**

### 🔬 5. Minute-by-Minute Fact-Check (NEW v2.5)
TruthGuard now queries the global **live news index** with a 24-hour strict filter. This allows the system to detect breaking news updates, live conference results, and ongoing disasters as they happen.

### ⚖️ 6. Automated Truth Correction (The Fact-Report)
When a "Fake" verdict is reached, the system automatically identifies the most reliable **Correction Source** from verified news organizations and features it at the top of the report to directly replace disinformation with facts.

---

## 🛠️ Modern Tech Stack

### Backend (The Forensic Core)
*   **Runtime:** Python 3.13 managed by **[uv](https://github.com/astral-sh/uv)**.
*   **Orchestration:** Custom `Orchestrator` managing concurrent `asyncio` agent tasks.
*   **Intelligence:** Hybrid Transformer models (`BERT`, `DistilBERT`) + Scikit-Learn.
*   **Scraping:** Newspaper3k + BeautifulSoup4 with high-speed threadpooling.
*   **Experience Engine:** Persistent `Tfidf` memory of past human-in-the-loop corrections.

### Frontend (The Research Dashboard)
*   **Framework:** React 18+ (Vite) with a clinical, dark industrial theme.
*   **UI/UX:** Real-time "Execution Trace" showing agent activities, neural trust meters, and adversarial argument cards.
*   **State:** Custom hooks for live-scanning states and investigation history.

---

## 🚀 Professional Setup Guide

### 1. Prerequisites
*   **Python 3.12+** & **Node.js 18+**.
*   Install **uv** for blazing fast backend performance: `pip install uv`.

### 2. Launch the Backend
```powershell
cd backend
uv sync
uv run python -m app
```
*(On first run, the system will download the BERT neural weights—this only happens once!)*

### 3. Launch the Frontend
```powershell
cd frontend
npm install
npm run dev
```

---

## 📊 Scientific Accuracy (Evaluation Mode)
TruthGuard 2.0 includes a **Benchmark System** (Upgrade 15) to scientifically measure Precision, Recall, and Accuracy. Developers can upload a labeled dataset to the `/evaluate` endpoint to see exactly how the multi-agent system performs against real-world misinformation.

---
*Built for the Truth. Engineered for the Future.*
