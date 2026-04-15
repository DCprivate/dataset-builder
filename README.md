# dataset-builder
Tool for scraping video, audio and text to be stored in a db and fed into a RAG.


[Web App UI] -----------\
                         --> [API Layer] --> [Agent Orchestrator]
[Desktop App UI/Tauri] --/         |                |
                                   |                |
                                   v                v
                             [Project/File Store] [Tool Runner]
                                   |                |
                                   v                v
                             [Retriever/Search] <-> [LLM Providers / Local Models]
                                   |
                                   v
                           [Rust Native Services]