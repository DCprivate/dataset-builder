Here are a few ways to create a list of installed packages or make a portable environment:

1. Generate requirements file from your active venv:

```bash
pip freeze > requirements.txt
```

2. For a more minimal requirements file (only direct dependencies):

```bash
pip-tools compile pyproject.toml -o requirements.txt
```

3. Create a portable venv:

```bash
# Create a new venv
python -m venv portable_venv

# Activate it
source portable_venv/bin/activate  # Linux/Mac
# or
.\portable_venv\Scripts\activate  # Windows

# Install packages from requirements
pip install -r requirements.txt

# Create archive
tar -czf portable_venv.tar.gz portable_venv/  # Linux/Mac
# or 
7z a portable_venv.zip portable_venv/  # Windows
```

4. For a clean dependency list in pyproject.toml:

```bash
# Install pip-audit to check dependencies
pip install pip-audit

# Generate dependency list
pip-audit --requirement requirements.txt --format json > dependencies.json
```

The most recommended approach is using `pip freeze > requirements.txt` since it captures exact versions of all dependencies.

















The error occurs because we need to run pip install from the correct directory. Try these commands:

```bash
# From the project root (Software/DataHarvester)
cd services/shared
pip install -e .
```

Also, let's update the package structure. First, move the existing files to the new structure:

```bash
# From services/shared directory
# Move mongodb files
mv src/mongodb/* src/dataharvester_shared/mongodb/
rm -rf src/mongodb

# Move config files
mv src/config/* src/dataharvester_shared/config/
rm -rf src/config

# Clean up old files
rm -f __init__.py
rm -f schemas.py
rm -f src/__init__.py
```

Your final directory structure should look like:
```
services/shared/
├── Dockerfile.shared
├── directory_tree.md
├── pyproject.toml
└── src/
    └── dataharvester_shared/
        ├── __init__.py
        ├── config/
        │   ├── __init__.py
        │   ├── celery_config.py
        │   └── settings.py
        ├── mongodb/
        │   ├── __init__.py
        │   ├── models.py
        │   └── repository.py
        └── schemas.py
```

Then update your imports in other services to use:
```python
from dataharvester_shared.mongodb.models import CleanedDocument
from dataharvester_shared.config.settings import get_settings
```

Would you like me to show the updated import paths for specific files?

