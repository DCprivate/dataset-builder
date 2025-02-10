#!/bin/bash

# Change to DataHarvester directory
cd ../DataHarvester

# Create virtual environment
python3.12 -m venv .venv

# Activate virtual environment (this varies by shell)
if [[ -n $BASH ]]; then
    source .venv/bin/activate
elif [[ -n $ZSH_NAME ]]; then
    source .venv/bin/activate
else
    echo "Please activate the virtual environment manually"
    exit 1
fi

# Verify we're in the venv
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Failed to activate virtual environment"
    exit 1
fi

# Install development packages first
pip install pydantic openai anthropic instructor

# Install requirements if files exist and are not empty
for service in data_transformation data_ingestion shared api; do
    if [ -s "services/$service/requirements.txt" ]; then
        pip install -r "services/$service/requirements.txt"
    fi
done

# Only try to install shared package if setup.py exists
if [ -f "services/shared/setup.py" ]; then
    cd services/shared
    pip install -e .
    cd ../..
fi

echo "Development environment setup complete!"