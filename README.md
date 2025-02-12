# DataHarvester: ML Model Fine-tuning Data Pipeline (placeholder)

## Overview
DataHarvester is an event-driven data pipeline system designed for collecting, processing, and preparing training data for ML model fine-tuning. The system operates locally without cloud dependencies and follows domain-driven design principles.

## Architecture
- **Event-Driven Architecture**: Loosely coupled services communicating via events
- **Microservices**: Independent, specialized services for data collection, processing, and transformation
- **Domain-Driven Design**: Business logic encapsulated within bounded contexts
- **Factory & Strategy Patterns**: For flexible component creation and processing algorithms

## Core Services

### Scraper Service
- Multi-threaded web scraping with rate limiting
- YouTube subtitle transcription
- Data validation and error recovery
- Scrapy/BeautifulSoup implementation

### Batch Processor Service
- Data cleaning and transformation
- Feature extraction
- Dataset creation
- Parallel processing capabilities

### MongoDB Service
- Document storage for processed data
- Metadata management
- Data versioning support

### Transformer Service
- Text processing and normalization
- Template-based transformations
- Quality validation

## Setup & Installation

### Prerequisites
- Python 3.12.8
- Docker & Docker Compose
- MongoDB
- Redis

### Quick Start
1. Clone the repository
2. Navigate to the project root
3. Run `docker compose -f compose/docker-compose.yml up -d`

## Project Structure
