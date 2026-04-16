# dataset-builder
Tool for scraping video, audio and text to be stored in a db and fed into a RAG.

Structure:

dataset-builder
├── ingest/
│   ├── web/
│   ├── youtube/
│   ├── documents/
│   ├── transcripts/
│   └── text/
├── normalize/
├── transform/
├── chunk/
├── embed/
└── load/

dataset_builder/
├── main.py
├── config.py
├── models/
│   └── normalized_document.py
├── ingest/
│   ├── base.py
│   ├── web_ingestor.py
│   ├── youtube_ingestor.py
│   ├── document_ingestor.py
│   └── text_ingestor.py
├── transform/
│   ├── cleaner.py
│   ├── deduper.py
│   └── sectionizer.py
├── rag/
│   ├── chunker.py
│   ├── embedder.py
│   └── loader.py
└── inputs/
    ├── web_urls.txt
    ├── youtube_urls.txt
    ├── documents/
    └── text/



Prerequisits:

pip install scrapy