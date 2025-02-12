# DataHarvester/README.md
// Start of Selection
# DataHarvester

A robust, pipeline-based architecture for collecting, transforming, and preparing data for ML model fine-tuning. Built with Python 3.12.8, MongoDB, and Redis, this framework provides modular microservices that follow domain-driven design principles. It's cloud-agnostic but can be seamlessly deployed on AWS or other container environments.

## Project Structure
```
DataHarvester/
├── services/
│   ├── api/              # FastAPI service
│   ├── caddy/            # Reverse proxy
│   ├── data_ingestion/   # Data collection service (scraping, ingestion)
│   ├── data_transformation/  # Data processing service (cleaning, transformations)
│   ├── database/         # MongoDB configuration
│   ├── shared/           # Shared utilities
│   └── worker/           # Celery worker service
├── compose/              # Docker compose files
├── data/                 # Data storage (raw, processed)
├── docs/                 # Documentation
├── logs/                 # Application logs
└── examples/             # Example outputs
```

## Development Setup

### Prerequisites
- Python 3.12.8
- pip 24.0 or higher
- venv (usually comes with Python)
- Docker and Docker Compose (for local container orchestration)

### Initial Setup

1. Create and activate virtual environment:
```bash
sudo apt install python3.12-venv

/usr/bin/python3.12 -m venv .venv

source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

2. Install development packages:
```bash
# Install shared package in editable mode
cd services/shared
pip install -e .
cd ..

# Install worker package in editable mode
cd worker
pip install -e .
cd ..

# Repeat for other services as needed
```

### VS Code Configuration

Create/update `.vscode/settings.json`:
```json
{
    "python.analysis.extraPaths": [
        "./services/shared/src"
    ],
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```

### Service Dependencies

Each microservice depends on the shared package, so install it first.

1. Install shared utilities:
```bash
cd services/shared
pip install -e .
cd ../..
```

2. Then install other service packages:
```bash
# API Service
cd services/api
pip install -e .
cd ../..

# Worker Service
cd services/worker
pip install -e .
cd ../..

# Data Ingestion Service
cd services/data_ingestion
pip install -e .
cd ../..

# Data Transformation Service
cd services/data_transformation
pip install -e .
cd ../..
```

Or use this one-liner to install all services:
```bash
for service in shared api worker data_ingestion data_transformation; do cd services/$service && pip install -e . && cd ../..; done
```

### Running Services

Using Docker Compose:
```bash
cd compose
docker-compose up --build
```
(If deploying to AWS, configure your infrastructure as code and container registry accordingly.)

### Dependency Auditing

To check for security vulnerabilities:
```bash
pip install pip-audit
pip-audit
```

## Documentation

See the `docs/` directory for pipeline details:
- `docs/to-do.md` - Project tasks and roadmap
- `docs/to-do-2.md` - Additional planned features

## Monitoring and Logs

- Application logs are stored in the `logs/` directory.
- Each service writes logs independently for better traceability.
- MongoDB data is persisted in Docker volumes; you can configure AWS S3 or another storage solution as needed for larger-scale workflows.