FROM python:3.9-slim

LABEL maintainer="ChemAI Discovery Team"
LABEL version="2.0.0"
LABEL description="Revolutionary AI-powered drug discovery platform"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs data/molecules models/pretrained

# Set environment variables
ENV PYTHONPATH=/app
ENV GPU_ENABLED=false
ENV MAX_WORKERS=4

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "src/main.py"]
