# Software/DataHarvester/services/data_ingestion/Dockerfile.DI

# Use Python 3.12.8 as specified in the requirements
FROM python:3.12.8-slim-bookworm

# Add labels for maintainability
LABEL maintainer="Jay-Alexander Elliot <11063158@uvu.edu>"
LABEL description="Data Ingestion service for DataHarvester"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install shared package first
COPY services/shared /shared
RUN pip install -e /shared

# Copy service code
COPY services/data_ingestion /app
RUN pip install -e .

# Install NLTK data and spaCy model
RUN python -m nltk.downloader -d /usr/local/share/nltk_data punkt stopwords words && \
    python -m spacy download en_core_web_sm

# Create necessary directories and set permissions
RUN mkdir -p /app/config /app/data/raw /app/data/processed /app/logs && \
    chmod -R 777 /app && \
    chmod -R 777 /usr/local/share/nltk_data

ENV PYTHONPATH=/app:/shared
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "data_ingestion.presentation.cli.main"]