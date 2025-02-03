# YouTube Subtitle Data Harvester

A robust data pipeline for harvesting, processing, and storing YouTube video subtitles. Built with Python 3.12.8 and MongoDB.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Directory Structure](#directory-structure)
- [Monitoring and Logs](#monitoring-and-logs)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Docker Engine (20.10.0 or higher)
- Docker Compose (2.0.0 or higher)
- At least 4GB of free RAM
- At least 10GB of free disk space

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Software/DataHarvester
```

2. Build the Docker images:
```bash
docker-compose -f docker/docker-compose.yml build
```

## Configuration

Before running the application, configure the following files in the `config` directory:

1. `urls.yaml`: Add YouTube video URLs, playlists, or channels to process
```yaml
urls:
  videos:
    - "https://www.youtube.com/watch?v=VIDEO_ID"
  playlists:
    - "https://www.youtube.com/playlist?list=PLAYLIST_ID"
  channels:
    - "https://www.youtube.com/channel/CHANNEL_ID"
```

2. `cleaning.yaml`: Configure text cleaning settings (default settings should work for most cases)

3. `database.yaml`: Configure MongoDB settings (default settings work with provided docker-compose)

## Running the Application

1. Start the services:
```bash
docker-compose -f docker/docker-compose.yml up -d
```

2. Monitor the logs:
```bash
docker-compose -f docker/docker-compose.yml logs -f scraper
```

3. Stop the services:
```bash
docker-compose -f docker/docker-compose.yml down
```

To remove all data and start fresh:
```bash
docker-compose -f docker/docker-compose.yml down -v
```

## Directory Structure

```
DataHarvester/
├── config/                 # Configuration files
├── data/                  # Data storage
│   ├── raw/              # Raw subtitle data
│   └── processed/        # Processed subtitle data
├── docker/               # Docker configuration
├── docs/                 # Documentation
├── logs/                 # Application logs
└── src/                  # Source code
    ├── core/            # Core functionality
    ├── infrastructure/  # Infrastructure components
    ├── monitoring/      # Monitoring utilities
    ├── services/        # Business logic services
    └── validation/      # Validation components
```

## Monitoring and Logs

- Application logs: `logs/youtube_scraper_*.log`
- Docker logs: `docker-compose -f docker/docker-compose.yml logs`
- MongoDB data: Persisted in docker volume `mongodb_data`

Health checks are automatically performed for:
- MongoDB connection
- NLTK data availability
- spaCy model availability
- Overall application health

## Troubleshooting

### Common Issues

1. MongoDB Connection Failed
```bash
# Check MongoDB status
docker-compose -f docker/docker-compose.yml ps mongo
# Check MongoDB logs
docker-compose -f docker/docker-compose.yml logs mongo
```

2. Missing NLTK Data
```bash
# Access the container
docker-compose -f docker/docker-compose.yml exec scraper bash
# Verify NLTK data
python -c "import nltk; nltk.data.path"
```

3. Permission Issues
```bash
# Fix permissions on host
sudo chown -R 1000:1000 logs/ data/
```

4. Container Won't Start
```bash
# Check container logs
docker-compose -f docker/docker-compose.yml logs scraper
# Verify health checks
docker inspect <container_id> | grep Health -A 10
```

### Data Management

To backup MongoDB data:
```bash
docker-compose -f docker/docker-compose.yml exec mongo mongodump --out /data/db/backup
```

To restore MongoDB data:
```bash
docker-compose -f docker/docker-compose.yml exec mongo mongorestore /data/db/backup
```

### Resource Usage

Monitor container resource usage:
```bash
docker stats $(docker-compose -f docker/docker-compose.yml ps -q)
```

## Environment Variables

The following environment variables can be modified in docker-compose.yml:

- `MONGO_URI`: MongoDB connection URI
- `MONGO_DB`: MongoDB database name
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)
- `PYTHONUNBUFFERED`: Python output buffering
- `NLTK_DATA`: NLTK data directory
- `SPACY_MODEL`: spaCy model name

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests (when implemented)
4. Submit a pull request