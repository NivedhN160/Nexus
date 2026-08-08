FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY apps/api/requirements.txt .
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Copy source code (this is mostly for production, docker-compose uses volumes for dev)
COPY apps/api /app/apps/api
COPY packages /app/packages

# Set python path
ENV PYTHONPATH=/app

CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
