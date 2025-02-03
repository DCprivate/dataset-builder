# Stage 1: Base image with Python and Chrome
FROM python:3.10.12-slim-buster AS python-chrome

# Install Chrome and its dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    apt-transport-https \
    ca-certificates \
    xvfb \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libasound2 \
    libxtst6 \
    libgtk-3-0 \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add virtual display
ENV DISPLAY=:99
RUN printf '#!/bin/bash\nXvfb :99 -screen 0 1920x1080x24 &\nexec "$@"\n' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

# Stage 2: Builder stage
FROM python-chrome AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Final stage
FROM python-chrome AS final

# Create non-root user with flexible UID/GID
RUN groupadd -r scraper && useradd -r -g scraper scraper

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

# Copy application code
COPY . .

# Create necessary directories with proper permissions
RUN mkdir -p downloads process tmp logs \
    && chown -R scraper:scraper /app \
    && chmod -R 755 /app \
    && chmod 777 downloads process tmp logs

# Switch to non-root user
USER scraper

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LOG_DIR=/app/logs \
    PATH="/app:${PATH}"

# Create volume mount points
VOLUME ["/app/downloads", "/app/process", "/app/logs"]

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh", "python", "main.py"] 