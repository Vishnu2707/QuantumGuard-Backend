# ---- QuantumGuard Backend Dockerfile ----
FROM python:3.11-slim

# Install build tools & liboqs dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates libssl-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY services/api/requirements.txt /app/requirements.txt

# Upgrade pip and install deps
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

COPY services/api /app

ENV PORT=8000
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
