# ⚙️ TruthGuard Backend: The Intelligence Engine

This is the core forensic engine for TruthGuard 2.5, powered by a multi-agent orchestration layer, high-speed neural classifiers, and a live web intelligence system.

## 🛠️ Architecture: The Agentic Pipeline
The backend follows a **Concurrent Orchestration** pattern:

1.  **ClaimAgent**: Decomposes user input into atomic facts.
2.  **WebAgent**: Generates optimized queries for **Live News** (24h filter).
3.  **ScraperAgent**: Extracts high-fidelity text from source URLs using threadpooling.
4.  **EvidenceAgent**: Performs semantic cross-comparison and neural classification.
5.  **BiasAgent**: Analyzes linguistic sentiment and emotional manipulation.
6.  **ReflectionAgent**: Performs a "Sanity Check" to ensure the final score is balanced.

## 🛡️ Security Features
*   **SSRF Protection**: Built-in validation to block access to internal/localhost IPs.
*   **Hardened Headers**: Automatic injection of `X-Frame-Options` and `X-Content-Type` security policies.
*   **Rate Limiting**: Intelligent IP-based throttling to prevent API abuse.
*   **Encapsulated Errors**: Sensitive system traces are kept in logs, while generalized responses are sent to the client.

## 📡 API Reference

### `POST /analyze`
The primary endpoint for total forensic investigation.
**Request:**
```json
{
  "text": "Your claim here",
  "url": "Optional direct article link"
}
```

### `POST /feedback`
Manual human-in-the-loop correction to train the **Experience Engine**.
```json
{
  "text": "Claim text",
  "label": "Real/Fake"
}
```

### `POST /generate_fake`
Research-only synthetic misinformation generator.

## 🚀 Setup & Development
1.  **Install uv**: `pip install uv`
2.  **Sync Dependencies**: `uv sync`
3.  **Run with Hot-Reload**: `uv run python app.py`

## 📊 Evaluation
You can run automated benchmarks by sending a labeled dataset to `/evaluate`. The engine will return Precision/Recall metrics based on the multi-agent consensus.
