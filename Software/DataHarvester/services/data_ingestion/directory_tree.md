jay@DESKTOP-N3AJ5U8:~/Github/CS-339R/Software/DataHarvester/services/data_ingestion$ tree
.
├── Dockerfile.DI
├── __init__.py
├── application
│   ├── __init__.py
│   └── services
│       ├── __init__.py
│       ├── text
│       │   ├── __init__.py
│       │   ├── nlp_service.py
│       │   └── text_cleaner_service.py
│       └── transcript
│           ├── __init__.py
│           ├── transcript_processor.py
│           └── transcript_service.py
├── directory_tree.md
├── domain
│   ├── __init__.py
│   ├── exceptions
│   │   ├── __init__.py
│   │   └── domain_exceptions.py
│   └── models
│       ├── __init__.py
│       └── transcript.py
├── infrastructure
│   ├── config
│   │   ├── __init__.py
│   │   └── config_manager.py
│   ├── error_handling
│   │   ├── __init__.py
│   │   ├── error_registry.py
│   │   ├── exceptions
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── specific.py
│   │   ├── handlers
│   │   │   ├── __init__.py
│   │   │   └── error_handler.py
│   │   ├── middleware
│   │   │   ├── __init__.py
│   │   │   └── error_middleware.py
│   │   └── utils
│   │       ├── __init__.py
│   │       ├── text_utils.py
│   │       └── time_utils.py
│   ├── logging
│   │   ├── __init__.py
│   │   └── logger.py
│   ├── monitoring
│   │   ├── __init__.py
│   │   └── health_checker.py
│   └── persistence
│       └── mongodb
│           ├── __init__.py
│           └── mongo_repository.py
├── presentation
│   ├── __init__.py
│   └── cli
│       ├── __init__.py
│       └── main.py
├── pyproject.toml
├── requirements.txt
└── validation
    ├── __init__.py
    ├── rules
    │   ├── __init__.py
    │   └── validation_rules.py
    └── validators
        ├── __init__.py
        ├── base_validator.py
        ├── config_validator.py
        ├── database_validator.py
        ├── scraping_validator.py
        └── youtube_validator.py

23 directories, 50 files
