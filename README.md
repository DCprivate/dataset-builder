# dataset-builder

A unified ingestion tool that converts mixed raw inputs into **RAG**.

The cleanest review order is:

models.py — what data exists in the system
config.py — what inputs/control knobs exist
registry.py — how source types map to ingesters
base.py — the ingestion contract
each ingester: text_source.py, pdf.py, web.py, youtube.py
chunking.py — how documents become chunks
pipeline.py — how everything is orchestrated
io.py — how outputs are written
embeddings.py — later, since you want to defer that
cli.py — last, once the internal flow makes sense

That order goes from data model → behavior → orchestration

## Supported inputs
- Websites / URL lists
- PDFs
- Plain text / markdown / notes
- YouTube videos (via transcript extraction)
- Textbook-like document inputs that can be parsed as PDF or plain text

## Output
The pipeline writes two layers:

1. **documents.jsonl**
   - one normalized document per source
   - preserves source metadata and raw extracted text

2. **chunks.jsonl** and **chunks.parquet**
   - retrieval-sized chunks
   - stable chunk ids
   - metadata usable by FAISS, Chroma, Qdrant, pgvector, Elasticsearch, etc.

Optional:

3. **embeddings.parquet**
   - generated with SentenceTransformers
   - ready to load into a vector store

## Why this shape
A clean RAG pipeline usually has distinct phases:
- ingestion/extraction
- normalization
- chunking
- embedding/indexing
- retrieval/generation

This repository handles the first four. It does **not** bundle a retriever or LLM wrapper into the same codepath.

## Depenencies

'''bash
pip install typer pydantic tqdm orjson pyyaml pypdf trafilatura youtube-transcript-api sentence_transformers
'''

## Installation

```bash

python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows PowerShell

pip install -e .
# optional embedding support
pip install -e .[embeddings]
```

## Example config
See `config/example.sources.yaml`.

## Run

```bash
dataset-builder build --config config/example.sources.yaml --output-dir output
```

## CLI shortcuts

```bash
# Build from config
dataset-builder build --config config/example.sources.yaml --output-dir output

# Add a single website directly
dataset-builder build --website https://example.com --output-dir output

# Add a PDF directly
dataset-builder build --pdf ./files/book.pdf --output-dir output

# Add a YouTube URL directly
dataset-builder build --youtube https://www.youtube.com/watch?v=dQw4w9WgXcQ --output-dir output

# Add a plain text file directly
dataset-builder build --text ./notes/chapter1.txt --output-dir output

# Create embeddings for produced chunks
dataset-builder embed --chunks output/chunks.parquet --model sentence-transformers/all-MiniLM-L6-v2
```

## Config format

```yaml
chunking:
  chunk_size: 900
  chunk_overlap: 150
  min_chunk_chars: 200

sources:
  - kind: website
    value: https://example.com/article
  - kind: pdf
    value: ./files/textbook.pdf
  - kind: text
    value: ./files/notes.txt
  - kind: youtube
    value: https://www.youtube.com/watch?v=VIDEO_ID
```

## Output schema

### documents.jsonl
```json
{
  "doc_id": "sha256...",
  "source_type": "pdf",
  "source_uri": "./files/textbook.pdf",
  "title": "Chapter 1",
  "text": "full normalized text...",
  "metadata": {
    "pages": 12,
    "author": "..."
  }
}
```

### chunks.jsonl
```json
{
  "chunk_id": "docid:0001",
  "doc_id": "sha256...",
  "text": "chunk text...",
  "token_estimate": 217,
  "metadata": {
    "source_type": "website",
    "source_uri": "https://example.com/article",
    "title": "Example article",
    "chunk_index": 1,
    "char_start": 0,
    "char_end": 878
  }
}
```

## Recommended downstream usage
- `documents.jsonl` for audit/debugging
- `chunks.parquet` as the canonical retrieval dataset
- embed `chunks.parquet`
- load embeddings into your vector store
- keep chunk metadata attached to every vector

## Notes
- Scanned/image-only PDFs may need OCR. This project first tries text-native extraction.
- YouTube transcripts depend on transcript availability.
- Website extraction focuses on main article/body content rather than full DOM capture
