#!/bin/bash
# Software/DataHarvester/services/api/app/start.sh

# Wait for MongoDB to be ready
sleep 5

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port 8080 --reload 