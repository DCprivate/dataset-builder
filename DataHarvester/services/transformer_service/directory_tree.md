(base) jay@MSI:~/GitHub/dataset-builder/DataHarvester/services/data_transformation$ tree
.
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

17 directories, 49 files