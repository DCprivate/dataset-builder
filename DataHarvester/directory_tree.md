(base) jay@MSI:~/GitHub/dataset-builder/DataHarvester$ tree
.
├── README.md
├── compose
│   └── docker-compose.yml
├── directory_tree.md
├── ideas.md
├── pyproject.toml
└── services
    ├── batch_processor
    │   ├── Dockerfile.celery
    │   ├── directory_tree.md
    │   ├── pipeline_worker
    │   │   ├── __init__.py
    │   │   ├── base.py
    │   │   ├── celery_config.py
    │   │   ├── registry.py
    │   │   ├── schemas.py
    │   │   ├── tasks.py
    │   │   └── validators.py
    │   └── pyproject.toml
    ├── mongo_service
    │   ├── Dockerfile.MongoDB
    │   ├── directory_tree.md
    │   ├── init_mongo.py
    │   ├── mongod.conf
    │   └── pyproject.toml
    ├── scraper_service
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
    │   │   └── monitoring
    │   │       ├── __init__.py
    │   │       └── health_checker.py
    │   ├── presentation
    │   │   ├── __init__.py
    │   │   └── cli
    │   │       ├── __init__.py
    │   │       └── cli_handler.py
    │   ├── pyproject.toml
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
    └── transformer_service
        ├── Dockerfile.DT
        ├── __init__.py
        ├── directory_tree.md
        ├── pyproject.toml
        └── src
            ├── domain
            │   ├── __init__.py
            │   ├── interfaces
            │   │   ├── __init__.py
            │   │   ├── base.py
            │   │   ├── repository.py
            │   │   └── schema.py
            │   ├── models.py
            │   └── services
            │       ├── __init__.py
            │       └── event.py
            ├── infrastructure
            │   ├── config
            │   │   ├── __init__.py
            │   │   └── llm_config.py
            │   ├── error_handling
            │   │   ├── __init__.py
            │   │   └── exceptions.py
            │   ├── mongodb
            │   │   ├── __init__.py
            │   │   ├── factory.py
            │   │   └── repository.py
            │   └── tasks
            │       ├── __init__.py
            │       └── task.py
            ├── interfaces
            │   ├── templates
            │   │   ├── CGSM-Project
            │   │   │   └── GRS-records.j2
            │   │   ├── Notes.md
            │   │   ├── __init__.py
            │   │   ├── neurodivergent
            │   │   │   ├── adhd_engagement.j2
            │   │   │   ├── autism_aspergers_interaction.j2
            │   │   │   ├── down_syndrome_communication.j2
            │   │   │   ├── dyslexia_reading_support.j2
            │   │   │   └── sensory_processing_regulation.j2
            │   │   ├── neurotypical
            │   │   │   ├── behavior_correction.j2
            │   │   │   ├── creative_task.j2
            │   │   │   ├── emotional_response.j2
            │   │   │   ├── group_activity_response.j2
            │   │   │   ├── interaction_classifier_template.j2
            │   │   │   ├── student_response_template.j2
            │   │   │   ├── subject_transition.j2
            │   │   │   └── teacher_followup_template.j2
            │   │   └── nt_responses
            │   │       ├── nt_communication_diff_response.j2
            │   │       ├── nt_curiosity_response.j2
            │   │       ├── nt_movement_diff_response.j2
            │   │       ├── nt_overstimulation_response.j2
            │   │       └── nt_special_interest_response.j2
            │   └── utils
            │       ├── __init__.py
            │       └── event_factory.py
            └── services
                ├── __init__.py
                ├── llm.py
                ├── llm_factory.py
                ├── prompt_loader.py
                └── validate.py

45 directories, 116 files