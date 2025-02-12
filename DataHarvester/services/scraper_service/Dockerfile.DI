# Software/DataHarvester/services/scraper_service/Dockerfile.DI

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
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the data ingestion service code
COPY services/scraper_service /app
RUN pip install -e .

# Install NLTK data
RUN python -m nltk.downloader -d /usr/local/share/nltk_data punkt stopwords words

# Create necessary directories
RUN mkdir -p /app/data/raw /app/logs && \
    chmod -R 777 /app/data /app/logs

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "scraper_service.main"]