# Headless Daemon Dockerfile for N.E.O.S
FROM python:3.10-slim

# Install system dependencies required for pyaudio, portaudio, and llama-cpp
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    libasound2-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1

# Note: You must mount the .gguf model file into /app/ via docker-compose or run arguments
CMD ["python", "daemon.py"]
