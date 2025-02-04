# /Software/DataHarvester/directory_tree.md

(.venv) (base) jay@MSI:~/GitHub/dataset-builder/Software/DataHarvester$ tree
.
├── README.md
├── compose
│   └── docker-compose.yml
├── data
├── directory_tree.md
├── docs
│   ├── directory_tree.md
│   ├── to-do-2.md
│   └── to-do.md
├── examples
│   └── output-example.json
├── logs
├── main.py
├── pyproject.toml
└── services
    ├── api
    │   ├── Dockerfile.api
    │   ├── app
    │   │   ├── dependencies.py
    │   │   ├── endpoints.py
    │   │   ├── main.py
    │   │   ├── schemas.py
    │   │   └── start.sh
    │   ├── dataharvester_api.egg-info
    │   │   ├── PKG-INFO
    │   │   ├── SOURCES.txt
    │   │   ├── dependency_links.txt
    │   │   ├── requires.txt
    │   │   └── top_level.txt
    │   ├── directory_tree.md
    │   └── pyproject.toml
    ├── caddy
    │   ├── Caddyfile
    │   ├── Dockerfile.caddy
    │   └── directory_tree.md
    ├── data_ingestion
    │   ├── Dockerfile.DI
    │   ├── __init__.py
    │   ├── application
    │   │   ├── __init__.py
    │   │   └── services
    │   │       ├── __init__.py
    │   │       ├── text
    │   │       │   ├── __init__.py
    │   │       │   ├── nlp_service.py
    │   │       │   └── text_cleaner_service.py
    │   │       └── transcript
    │   │           ├── __init__.py
    │   │           ├── transcript_processor.py
    │   │           └── transcript_service.py
    │   ├── data_ingestion.egg-info
    │   │   ├── PKG-INFO
    │   │   ├── SOURCES.txt
    │   │   ├── dependency_links.txt
    │   │   ├── requires.txt
    │   │   └── top_level.txt
    │   ├── directory_tree.md
    │   ├── domain
    │   │   ├── __init__.py
    │   │   ├── exceptions
    │   │   │   ├── __init__.py
    │   │   │   └── domain_exceptions.py
    │   │   └── models
    │   │       ├── __init__.py
    │   │       └── transcript.py
    │   ├── infrastructure
    │   │   ├── config
    │   │   │   ├── __init__.py
    │   │   │   └── config_manager.py
    │   │   ├── error_handling
    │   │   │   ├── __init__.py
    │   │   │   ├── error_registry.py
    │   │   │   ├── exceptions
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── base.py
    │   │   │   │   └── specific.py
    │   │   │   ├── handlers
    │   │   │   │   ├── __init__.py
    │   │   │   │   └── error_handler.py
    │   │   │   ├── middleware
    │   │   │   │   ├── __init__.py
    │   │   │   │   └── error_middleware.py
    │   │   │   └── utils
    │   │   │       ├── __init__.py
    │   │   │       ├── text_utils.py
    │   │   │       └── time_utils.py
    │   │   ├── logging
    │   │   │   ├── __init__.py
    │   │   │   └── logger.py
    │   │   ├── monitoring
    │   │   │   ├── __init__.py
    │   │   │   └── health_checker.py
    │   │   └── persistence
    │   │       └── mongodb
    │   │           ├── __init__.py
    │   │           └── mongo_repository.py
    │   ├── presentation
    │   │   ├── __init__.py
    │   │   └── cli
    │   │       ├── __init__.py
    │   │       └── main.py
    │   ├── pyproject.toml
    │   ├── setup.py
    │   └── validation
    │       ├── __init__.py
    │       ├── rules
    │       │   ├── __init__.py
    │       │   └── validation_rules.py
    │       └── validators
    │           ├── __init__.py
    │           ├── base_validator.py
    │           ├── config_validator.py
    │           ├── database_validator.py
    │           ├── scraping_validator.py
    │           └── youtube_validator.py
    ├── data_transformation
    │   ├── Dockerfile.DT
    │   ├── __init__.py
    │   ├── directory_tree.md
    │   ├── pyproject.toml
    │   └── src
    │       ├── application
    │       │   └── services
    │       │       ├── __init__.py
    │       │       ├── llm.py
    │       │       ├── llm_factory.py
    │       │       ├── prompt_loader.py
    │       │       └── validate.py
    │       ├── data_transformation.egg-info
    │       │   ├── PKG-INFO
    │       │   ├── SOURCES.txt
    │       │   ├── dependency_links.txt
    │       │   ├── requires.txt
    │       │   └── top_level.txt
    │       ├── domain
    │       │   ├── interfaces
    │       │   │   ├── __init__.py
    │       │   │   ├── base.py
    │       │   │   ├── repository.py
    │       │   │   └── schema.py
    │       │   └── services
    │       │       ├── __init__.py
    │       │       └── event.py
    │       ├── infrastructure
    │       │   ├── config
    │       │   │   ├── __init__.py
    │       │   │   └── llm_config.py
    │       │   ├── error_handling
    │       │   │   ├── __init__.py
    │       │   │   └── exceptions.py
    │       │   ├── persistence
    │       │   │   └── mongodb
    │       │   │       ├── __init__.py
    │       │   │       ├── factory.py
    │       │   │       └── repository.py
    │       │   └── tasks
    │       │       ├── __init__.py
    │       │       └── task.py
    │       └── interfaces
    │           ├── templates
    │           │   ├── CGSM-Project
    │           │   │   ├── GRS-records.j2
    │           │   │   └── __init__.py
    │           │   ├── Notes.md
    │           │   ├── __init__.py
    │           │   ├── neurodivergent
    │           │   │   ├── __init__.py
    │           │   │   ├── adhd_engagement.j2
    │           │   │   ├── autism_aspergers_interaction.j2
    │           │   │   ├── down_syndrome_communication.j2
    │           │   │   ├── dyslexia_reading_support.j2
    │           │   │   └── sensory_processing_regulation.j2
    │           │   ├── neurotypical
    │           │   │   ├── __init__.py
    │           │   │   ├── behavior_correction.j2
    │           │   │   ├── creative_task.j2
    │           │   │   ├── emotional_response.j2
    │           │   │   ├── group_activity_response.j2
    │           │   │   ├── interaction_classifier_template.j2
    │           │   │   ├── student_response_template.j2
    │           │   │   ├── subject_transition.j2
    │           │   │   └── teacher_followup_template.j2
    │           │   └── nt_responses
    │           │       ├── __init__.py
    │           │       ├── nt_communication_diff_response.j2
    │           │       ├── nt_curiosity_response.j2
    │           │       ├── nt_movement_diff_response.j2
    │           │       ├── nt_overstimulation_response.j2
    │           │       └── nt_special_interest_response.j2
    │           └── utils
    │               ├── __init__.py
    │               └── event_factory.py
    ├── database
    │   ├── Dockerfile.MongoDB
    │   ├── directory_tree.md
    │   ├── init-mongo.js
    │   └── mongod.conf
    ├── shared
    │   ├── Dockerfile.shared
    │   ├── __init__.py
    │   ├── directory_tree.md
    │   ├── pyproject.toml
    │   └── src
    │       ├── __init__.py
    │       ├── dataharvester_shared
    │       │   ├── __init__.py
    │       │   ├── config
    │       │   │   ├── celery_config.py
    │       │   │   └── settings.py
    │       │   ├── mongodb
    │       │   │   ├── __init__.py
    │       │   │   ├── models.py
    │       │   │   └── repository.py
    │       │   └── schemas.py
    │       └── dataharvester_shared.egg-info
    │           ├── PKG-INFO
    │           ├── SOURCES.txt
    │           ├── dependency_links.txt
    │           ├── requires.txt
    │           └── top_level.txt
    └── worker
        ├── Dockerfile.celery
        ├── directory_tree.md
        ├── pipeline_worker
        │   ├── base.py
        │   ├── celery_config.py
        │   ├── registry.py
        │   └── tasks.py
        ├── pipeline_worker.egg-info
        │   ├── PKG-INFO
        │   ├── SOURCES.txt
        │   ├── dependency_links.txt
        │   ├── requires.txt
        │   └── top_level.txt
        └── pyproject.toml

67 directories, 168 files
(.venv) (base) jay@MSI:~/GitHub/dataset-builder/Software/DataHarvester$ 