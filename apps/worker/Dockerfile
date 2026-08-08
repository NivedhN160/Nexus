FROM python:3.11-slim

WORKDIR /app

COPY apps/worker/requirements.txt .
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Copy source code (this is mostly for production, docker-compose uses volumes for dev)
COPY apps/worker /app/apps/worker
COPY apps/api /app/apps/api
COPY packages /app/packages

ENV PYTHONPATH=/app

CMD ["python", "apps/worker/main.py"]
