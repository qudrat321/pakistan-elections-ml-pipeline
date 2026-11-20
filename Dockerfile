# Base image: Python 3.12 slim for lightweight, production-ready deployment
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered output for real-time logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set container working directory
WORKDIR /app

# Install lightweight system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manifest and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code, trained model artifact, data, and frontend UI
COPY src/ ./src/
COPY models/ ./models/
COPY data/cleaned/ ./data/cleaned/
COPY frontend/ ./frontend/

# Expose port 7860 (Standard default for Hugging Face Spaces Docker SDK & Render)
EXPOSE 7860

# Run FastAPI backend via Uvicorn (supports Render $PORT and Hugging Face 7860)
CMD ["sh", "-c", "uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-7860}"]
