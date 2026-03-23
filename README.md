# 🛡️ TruthGuard: AI-Powered Fake News Detection

![TruthGuard Banner](https://img.shields.io/badge/Status-Development-orange) ![License](https://img.shields.io/badge/License-MIT-green) ![Cost](https://img.shields.io/badge/Cost-$0%20(Free)-blue)

## 📌 Project Overview
TruthGuard is an advanced, high-performance Machine Learning pipeline designed to detect and classify fabricated news articles, misinformation, and clickbait. Developed as a final-year college project, it leverages deep Natural Language Processing (NLP) to provide real-time credibility scoring for text and URLs.

## ✨ Core Features
- **Real-Time Text Analysis:** Paste any news article to instantly receive a "Fake" or "Real" confidence score.
- **Explainable AI (XAI):** Highlights specific words and rhetorical patterns that influenced the model's decision.
- **URL Scraping:** Automatically bypasses ads to extract and analyze text directly from live news websites.
- **Premium User Interface:** A blazing-fast, modern, glassmorphic dashboard built for seamless user experience.

## 🛠️ Tech Stack (100% Free & Open-Source)
Everything in this project is built using free, open-source tools—requiring **zero financial investment**.

### Frontend (Client-Side)
- **Framework:** React (via Vite) for a lightning-fast Single Page Application.
- **Styling:** Vanilla CSS (Custom modern animations, dark mode, no bloated frameworks).
- **Hosting (Free):** Vercel or GitHub Pages.

### Backend (Server-Side)
- **Framework:** FastAPI (Python) - asynchronous and highly performant.
- **Scraping:** BeautifulSoup4 & Newspaper3k (Free web scraping).
- **Hosting (Free):** Render, Pythonanywhere, or Hugging Face Spaces.

### Machine Learning (The Core)
- **Language:** Python 3.10+
- **NLP Libraries:** NLTK, spaCy.
- **Algorithms:** TF-IDF Vectorizer + Passive-Aggressive Classifier (or Scikit-learn Logistic Regression).
- **Dataset (Free):** ISOT Fake News Dataset / Kaggle.

### Architecture & Performance
- **Database:** SQLite (Built-in, local, $0 cost).
- **Caching:** In-memory LRU Cache (To remember previously scanned viral articles for instant results without re-running the ML model).

## 🚀 Future Enhancements (Phase 2)
- Multi-modal detection (analyzing images within the articles).
- Chrome Extension for live browsing alerts.
- Source credibility database (Domain scoring).

---
*Created for final-year submission. Designed with performance, scalability, and zero-cost deployment in mind.*
