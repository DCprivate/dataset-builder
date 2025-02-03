(base) jay@MSI:~/GitHub/CS-339R/Software$ tree -I 'logs'
.
├── DataHarvester
│   ├── README.md
│   ├── config
│   │   ├── cleaning.yaml
│   │   ├── database.yaml
│   │   ├── harvesting.yaml
│   │   └── sources.yaml
│   ├── data
│   │   ├── example.json
│   │   └── processed
│   ├── directory_tree.md
│   ├── docker
│   │   ├── Dockerfile.DataHarvester
│   │   └── docker-compose.yml
│   ├── examples
│   │   └── output-example.json
│   ├── main.py
│   ├── requirements.txt
│   ├── services
│   │   ├── External_LLM
│   │   ├── api
│   │   ├── caddy
│   │   ├── celery_worker
│   │   ├── database
│   │   └── dataharvester
│   ├── src
│   │   ├── core
│   │   │   ├── config.py
│   │   │   ├── exceptions.py
│   │   │   └── logging.py
│   │   ├── infrastructure
│   │   │   ├── database
│   │   │   │   ├── models.py
│   │   │   │   └── mongo_client.py
│   │   │   └── error_handling
│   │   │       ├── error_registry.py
│   │   │       ├── exceptions
│   │   │       │   ├── base.py
│   │   │       │   └── specific.py
│   │   │       ├── handlers
│   │   │       │   └── error_handler.py
│   │   │       ├── middleware
│   │   │       │   └── error_middleware.py
│   │   │       └── utils
│   │   │           ├── text_utils.py
│   │   │           └── time_utils.py
│   │   ├── monitoring
│   │   │   └── health.py
│   │   ├── services
│   │   │   ├── text
│   │   │   │   ├── cleaner.py
│   │   │   │   └── nlp.py
│   │   │   └── transcript
│   │   │       ├── processor.py
│   │   │       └── transcript_fetcher.py
│   │   └── validation
│   │       ├── base_validator.py
│   │       ├── config_rules.py
│   │       ├── database_rules.py
│   │       ├── scraping_rules.py
│   │       └── validators.py
│   ├── tests
│   │   └── to-do.md
│   └── to-do.md
├── Subscraper
│   ├── Dockerfile
│   ├── README.md
│   ├── docker-compose.yml
│   ├── main.py
│   ├── requirements.txt
│   ├── run.sh
│   ├── setup.sh
│   ├── src
│   │   ├── __init__.py
│   │   ├── api_client.py
│   │   ├── base_scraper.py
│   │   ├── downloader.py
│   │   ├── element_locations.py
│   │   ├── exceptions.py
│   │   ├── main_operations.py
│   │   ├── opensubtitles.py
│   │   ├── parsing.py
│   │   ├── scraper_manager.py
│   │   ├── url_parser.py
│   │   └── web_scraper.py
│   └── subscraper.py
└── scripts
    └── script.sh

31 directories, 57 files
(base) jay@MSI:~/GitHub/CS-339R/Software$ 