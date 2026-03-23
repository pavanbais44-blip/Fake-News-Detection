# Use highly optimized uv image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies into the container
RUN uv sync --frozen --no-dev

# Copy the rest of the application
COPY app ./app

# Expose FastAPI port
EXPOSE 8000

# Run the project using uv
CMD ["uv", "run", "python", "-m", "app.main"]
