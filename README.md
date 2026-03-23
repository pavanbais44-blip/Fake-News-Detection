# 🛡️ TruthGuard: Hybrid BERT-Powered Truth Engine

![TruthGuard Banner](https://img.shields.io/badge/Status-Production--Ready-brightgreen) ![License](https://img.shields.io/badge/License-MIT-green) ![Engine](https://img.shields.io/badge/Intelligence-BERT_Neural_Net-blue) ![Performance](https://img.shields.io/badge/Speed-Optimized_via_uv-orange)

## 📌 Project Overview
TruthGuard is a state-of-the-art **Fake News Identification Platform** that combines **Deep Learning (BERT)** with **Real-Time Global Verification**. Unlike standard classifiers that only look at word patterns, TruthGuard "understands" the context of news articles and crawls live news databases to find supporting evidence.

Developed as a high-performance final-year project, it offers a professional-grade solution to the problem of digital misinformation.

---

## ✨ Core Intelligent Features

### 🧠 1. BERT Neural Scan (Contextual Analysis)
Instead of simple word counts, TruthGuard uses an **Advanced Transformer (BERT)** model to analyze the linguistic DNA of an article. It can detect:
*   **Manipulation Patterns:** Phrases and structures common in propaganda.
*   **Contextual Sarcasm:** Identifying ironical or satirical tones.
*   **Nuanced Disinformation:** Catching subtle lies that traditional models miss.

### 📡 2. Live Cross-Reference (The "Ground Truth" Layer)
TruthGuard doesn't work in a vacuum. When you scan a claim, the engine:
1.  Extracts core keywords (Nouns/Verbs).
2.  Searches global news databases via **DuckDuckGo** in real-time.
3.  Cross-references your input with **Verified News Sources** (BBC, Reuters, AP, etc.).
4.  Provides a **"Verification Boost"** if the story is confirmed by official reporting.

### ⚖️ 3. Neural Sentiment & Bias Meter
Misinformation is often highly emotional. TruthGuard uses a specialized **Sentiment BERT** to measure:
*   **Polarity:** Is the tone intensely positive or aggressive?
*   **Subjectivity/Bias:** Does the article read like a fact or a heavily biased opinion?

---

## 🛠️ Modern Tech Stack

### Backend (The Intelligence Hub)
*   **Runtime:** Python 3.12+ managed by **[uv](https://github.com/astral-sh/uv)** (Blazing fast local environment).
*   **API:** FastAPI (Asynchronous & type-safe).
*   **AI Models:** 
    *   `bert-tiny-finetuned-fake-news-detection` (Efficient context classifier).
    *   `distilbert-base-uncased-finetuned-sst-2-english` (Advanced sentiment).
*   **Scraping:** Newspaper3k & BeautifulSoup4.

### Frontend (The Dashboard)
*   **Framework:** React 18+ (Vite) for a logic-heavy, lightning-fast UI.
*   **Design:** Premium Glassmorphic / Bento-Grid layout with vanilla CSS animations.
*   **Visuals:** Real-time circular trust meters and dynamic bias charts.

---

## 🚀 Instant Setup Guide

### 1. Prerequisites
Ensure you have **Python 3.12+** and **Node.js** installed.
You must also have **uv** installed (`pip install uv`).

### 2. Launch the Backend
```powershell
cd backend
uv sync
uv run app.py
```
*(On first run, the system will download ~100MB of BERT neural weights—this only happens once!)*

### 3. Launch the Frontend
```powershell
cd frontend
npm install
npm run dev
```

---

## 🔗 Architecture Logic
The "Truth Score" is calculated using a **Weighted Hybrid Formula**:
Score = (BERT_Score * 0.7) + (Live_Evidence_Boost * 0.3) - Subjectivity_Penalty

This ensures that even if a stylistic pattern looks "Real," the absence of global news coverage for a major claim will still result in a **"Suspicious"** or **"High-Risk"** alert.

---
*Developed for excellence. Built for Truth.*
