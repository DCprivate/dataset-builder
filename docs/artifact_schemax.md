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

## Validation rules by artifact

### 1. `documents.jsonl`

Each record must contain:

- `artifact_version`: string
- `doc_id`: string
- `source_type`: string
- `source_uri`: string
- `title`: string or null
- `text`: string
- `metadata`: object

---

### 2. `chunks.jsonl`

Each record must contain:

- `artifact_version`: string
- `chunk_id`: string
- `doc_id`: string
- `text`: string
- `token_estimate`: integer
- `metadata`: object

---

### 3. `embeddings.jsonl`

Each record must contain:

- `artifact_version`: string
- `chunk_id`: string
- `doc_id`: string
- `embedding`: array
- `metadata`: object

#### Additional embedding requirements

- `embedding` must be a non-empty array
- every element in `embedding` must be numeric (`int` or `float`)
- all embedding vectors in the same file should have the same dimensionality

---

### 4. `failures.jsonl`

Each record must contain:

- `artifact_version`: string
- `kind`: string
- `value`: string
- `error`: string

This file is mainly for diagnostics and does not usually participate in retrieval.

---

## Referential integrity checks

After loading records, `researchAI` should also validate references:

- every `chunk.doc_id` should exist in `documents.jsonl`
- every `embedding.chunk_id` should exist in `chunks.jsonl`
- every `embedding.doc_id` should exist in `documents.jsonl`

If these relationships are broken, loading should fail.
