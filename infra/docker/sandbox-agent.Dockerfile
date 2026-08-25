# DevCorp AI — Ephemeral Agent Execution Sandbox
FROM ubuntu:24.04

# Prevent interactive prompts during apt install
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install baseline developer dependencies, Python 3.12, Node.js 20, Git
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    ca-certificates \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    libpq-dev \
    pkg-config \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Create non-root developer user
RUN useradd -m -s /bin/bash developer && \
    mkdir -p /workspace && \
    chown -R developer:developer /workspace

USER developer
WORKDIR /workspace

# Install common Python tooling in user environment
RUN python3 -m pip install --no-cache-dir --break-system-packages \
    pytest \
    pytest-asyncio \
    ruff \
    mypy \
    fastapi \
    uvicorn \
    pydantic \
    httpx

# Default entrypoint: keep container alive for DSH session execution
CMD ["tail", "-f", "/dev/null"]
