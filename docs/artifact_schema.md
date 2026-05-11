# Artifact Schema

This document defines the file contract between `dataset-builder` and downstream consumers such as `researchAI`.

`dataset-builder` is the producer of these artifacts.  
`researchAI` is a consumer of these artifacts.

The goal of this contract is to keep the two repos separate while ensuring they agree on file shape and required fields.

---

## Versioning

All artifact records should include:

- `artifact_version`

Current version:

- `artifact_version = "1.0"`

If the structure changes in a breaking way, increment the version.

---

## Artifact overview

Current artifacts:

- `documents.jsonl`
- `chunks.jsonl`
- `embeddings.jsonl`
- `failures.jsonl`

Each file is newline-delimited JSON (**JSONL**).  
Each line is one complete JSON object.

---

## 1. `documents.jsonl`

### Purpose

Stores one normalized document per ingested source.

### Record schema

```json
{
  "artifact_version": "1.0",
  "doc_id": "string",
  "source_type": "string",
  "source_uri": "string",
  "title": "string or null",
  "text": "string",
  "metadata": {}
}