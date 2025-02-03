#!/bin/bash

# Create main directory structure
mkdir -p Software/DataHarvester/{src,config,docs,tests,docker}

# Create src subdirectories
cd Software/DataHarvester/src
mkdir -p {core,infrastructure/{database,error_handling},services/{content,text},validation,monitoring}

# Create __init__.py files
touch core/__init__.py
touch infrastructure/__init__.py
touch infrastructure/database/__init__.py
touch infrastructure/error_handling/__init__.py
touch services/__init__.py
touch services/content/__init__.py
touch services/text/__init__.py
touch validation/__init__.py
touch monitoring/__init__.py

# Create core files
touch core/{exceptions,config,logging}.py

# Create infrastructure files
touch infrastructure/database/{mongo_client,models}.py
touch infrastructure/error_handling/{handler,retries}.py

# Create service files
touch services/content/{extractor,processor}.py
touch services/text/{cleaner,nlp}.py

# Create validation files
touch validation/{base,config_rules,database_rules,harvesting_rules}.py

# Create monitoring files
touch monitoring/health.py

# Create config files
cd ../config
touch {database,harvesting,cleaning,sources}.yaml

# Create docker files
cd ../docker
touch {Dockerfile,docker-compose.yml}

# Create tests directory structure
cd ../tests
mkdir -p {core,infrastructure,services,validation,monitoring}
touch {core,infrastructure,services,validation,monitoring}/__init__.py

echo "Project structure created successfully!"