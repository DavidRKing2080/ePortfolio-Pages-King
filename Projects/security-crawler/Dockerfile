# Dockerfile
FROM python:3.11-slim

# Install minimal system deps (faster SSL/DNS, and pip)
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src ./src

# Default entrypoint: run the module
ENTRYPOINT ["python", "-m", "src.app"]
