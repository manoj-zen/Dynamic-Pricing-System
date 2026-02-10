# Multi-stage Dockerfile for Cloud Run deployment
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application files
COPY backend/ .

# Create data directory if not exists
RUN mkdir -p data

# Copy data files
COPY backend/data/ data/

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run FastAPI with Gunicorn
CMD exec gunicorn --bind :$PORT --workers 4 --timeout 120 --worker-class uvicorn.workers.UvicornWorker app:app
