FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# ⚙️ Set Python and UV Environments
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 🛠️ Install OS Dependencies (for newspaper3k/lxml)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# 📦 Dependency Sync
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

# 📥 Pre-fetch Neural & Lexical Data
RUN uv run python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"

# 🏁 Final Code Injection
COPY . .

EXPOSE 8000

# 🚀 Launch Agentic Lab
CMD ["uv", "run", "python", "app.py"]
