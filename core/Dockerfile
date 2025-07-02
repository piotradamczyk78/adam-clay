FROM python:3.11-slim

# Metadata
LABEL name="Adam Clay" \
      version="0.1.0" \
      description="First Autonomous AI Freelancer" \
      author="Adam Clay (AI) & Piotr Adamczyk (Human)"

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config.json main.py ./

# Create data directories
RUN mkdir -p data/thoughts data/conversations data/projects data/logs

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash adamclay && \
    chown -R adamclay:adamclay /app
USER adamclay

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Expose port (for future web interface)
EXPOSE 8000

# Default command
CMD ["python", "main.py"]

# Alternative commands for different modes:
# docker run adam-clay:latest python main.py --mode=consciousness
# docker run adam-clay:latest python main.py --mode=business
# docker run adam-clay:latest python main.py --mode=debug 