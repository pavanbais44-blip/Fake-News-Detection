# 🔬 TruthGuard Frontend: The Forensic Dashboard

This is the interface for researchers to interact with the TruthGuard Agentic Core. It is designed to provide maximum transparency during the misinformation investigation process.

## 🌟 Key Features

### 🚦 1. Real-Time Investigation Trace
Watch each agent (Claim, Web, Scraper, Evidence, Bias, Reflection) execute in real-time. The dashboard synchronizes with the backend's parallel processing states.

### ⚖️ 2. Neural Debate Arena
Visualizing the internal conflict:
*   **Agent ALPHA**: Supporting arguments derived from evidence.
*   **Agent OMEGA**: Disinformation/Propaganda patterns detected.
*   **Chief Justice**: The final reasoned verdict.

### 🛡️ 3. Hallucination Guard
A confidence-aware indicator that flags when the AI doesn't have enough data to be certain, preventing "certainty bias" in uncertain situations.

### 🧬 4. Atomic Claim Breakdown
Every paragraph is split into individual claims, showing you which specific part of a story is true and which is false.

## 🚀 Getting Started

1.  **Dependencies**: `npm install`
2.  **Dev Mode**: `npm run dev`
3.  **Production Build**: `npm run build`

## 🛠️ Configuration
The API connection is managed in `src/services/api.js`. Ensure the backend is running at `http://localhost:8000`.

## 🎨 Theme
The dashboard uses a **Clinical Dark Industrial** aesthetic:
*   **Real**: Emerald (#10b981)
*   **Fake**: Rose (#f43f5e)
*   **Accent**: Indigo/Violet Gradient
*   **Glassmorphism**: UI elements use heavy blur (20px) for a premium, forensic feel.
