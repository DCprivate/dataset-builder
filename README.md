# dataset-builder
Offline ingestion and indexing pipeline.
Produces normalized documents, chunks, embeddings, and indexed knowledge for researchAI

Structure:

dataset-builder
├── ingest/
│   ├── web/
│   ├── youtube/
│   ├── documents/
│   ├── transcripts/
│   └── text/
├── normalize/
├── chunk/
├── embed/
└── load/


Prerequisits:

pip install scrapy