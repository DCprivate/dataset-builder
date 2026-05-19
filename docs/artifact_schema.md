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
  "artifact_version": "float",
  "doc_id": "string",
  "source_type": "string",
  "source_uri": "string",
  "title": "string or null",
  "text": "string",
  "metadata": {}
}
```

### Notes

- `doc_id` must uniquely identify the normalized document
- `source_type` examples:
  - `"text"`
  - `"pdf"`
  - `"website"`
  - `"youtube"`
- `source_uri` is the original source locator:
  - file path for local files
  - URL for remote sources
- `metadata` is source-specific and may vary by ingester

### Example

```json
{
  "artifact_version": "1.0",
  "doc_id": "abc123",
  "source_type": "pdf",
  "source_uri": "examples/book.pdf",
  "title": "Chapter 1",
  "text": "Full normalized text goes here...",
  "metadata": {
    "path": "examples/book.pdf",
    "pages": 12
  }
}
```

---

## 2. `chunks.jsonl`

### Purpose

Stores retrieval-sized chunks derived from normalized documents.

### Record schema

```json
{
  "artifact_version": "1.0",
  "chunk_id": "string",
  "doc_id": "string",
  "text": "string",
  "token_estimate": 123,
  "metadata": {}
}
```

### Notes

- `chunk_id` must uniquely identify the chunk
- `doc_id` must reference a valid document in `documents.jsonl`
- `text` is the chunk text used for retrieval and embedding
- `token_estimate` is an approximate token count
- `metadata` should remain relatively small and useful for retrieval/citation

### Recommended chunk metadata fields

Recommended keys inside `metadata`:

- `source_type`
- `source_uri`
- `title`
- `chunk_index`

Optional later keys:

- `char_start`
- `char_end`
- `page_start`
- `page_end`

### Example

```json
{
  "artifact_version": "1.0",
  "chunk_id": "abc123:0001",
  "doc_id": "abc123",
  "text": "This is the text of the first chunk...",
  "token_estimate": 210,
  "metadata": {
    "source_type": "pdf",
    "source_uri": "examples/book.pdf",
    "title": "Chapter 1",
    "chunk_index": 1
  }
}
```

---

## 3. `embeddings.jsonl`

### Purpose

Stores embeddings for chunks.

### Record schema

```json
{
  "artifact_version": "float",
  "chunk_id": "string",
  "doc_id": "string",
  "embedding": [0.1, -0.2, 0.3],
  "metadata": {}
}
```

### Notes

- `chunk_id` must reference a valid chunk in `chunks.jsonl`
- `doc_id` must reference a valid document in `documents.jsonl`
- `embedding` is the dense vector representation of the chunk text
- `metadata` should be minimal and useful for lookup/filtering
- chunk text should usually **not** be duplicated here if `chunks.jsonl` is available

### Recommended embedding metadata fields

Recommended keys inside `metadata`:

- `source_type`
- `source_uri`
- `title`
- `chunk_index`

Optional additional keys:

- `embedding_model`
- `embedding_dim`

### Example

```json
{
  "artifact_version": "1.0",
  "chunk_id": "abc123:0001",
  "doc_id": "abc123",
  "embedding": [0.012, -0.442, 0.187],
  "metadata": {
    "source_type": "pdf",
    "source_uri": "examples/book.pdf",
    "title": "Chapter 1",
    "chunk_index": 1,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
  }
}
```

---

## 4. `failures.jsonl`

### Purpose

Stores ingestion or processing failures without stopping the entire pipeline.

### Record schema

```json
{
  "artifact_version": "float",
  "kind": "string",
  "value": "string",
  "error": "string"
}
```

### Notes

- `kind` is the source type that failed
- `value` is the original source value passed to the ingester
- `error` is the exception/error message

### Example

```json
{
  "artifact_version": "1.0",
  "kind": "pdf",
  "value": "examples/bad.pdf",
  "error": "No text extracted from PDF"
}
```

---

## Referential integrity rules

Consumers should assume the following:

- every `chunk.doc_id` should exist in `documents.jsonl`
- every `embedding.chunk_id` should exist in `chunks.jsonl`
- every `embedding.doc_id` should exist in `documents.jsonl`

`researchAI` should validate these assumptions when loading artifacts.

---

## Consumer expectations for `researchAI`

At minimum, `researchAI` should validate:

### For `chunks.jsonl`

- `artifact_version` exists and is supported
- `chunk_id` exists and is a string
- `doc_id` exists and is a string
- `text` exists and is a string
- `token_estimate` exists and is an integer
- `metadata` exists and is an object

### For `embeddings.jsonl`

- `artifact_version` exists and is supported
- `chunk_id` exists and is a string
- `doc_id` exists and is a string
- `embedding` exists and is an array
- every element in `embedding` is numeric
- `metadata` exists and is an object

---

## Runtime validation requirements (`researchAI`)

`researchAI` must validate artifact files when loading them.

The goal is to fail **early and clearly** if artifacts are missing fields, have the wrong types, or use an unsupported schema version.

Validation should happen before retrieval begins.

---

### Validation goals

When loading artifacts, `researchAI` should verify:

- the file exists
- each line is valid JSON
- each record contains all required fields
- each field has the expected type
- `artifact_version` is supported
- references between files are consistent where applicable

If validation fails, `researchAI` should raise a clear error immediately.

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

#### Example validation checks

- reject records with missing `doc_id`
- reject records where `text` is not a string
- reject records where `metadata` is not an object/dictionary
- reject records with unsupported `artifact_version`

---

### 2. `chunks.jsonl`

Each record must contain:

- `artifact_version`: string
- `chunk_id`: string
- `doc_id`: string
- `text`: string
- `token_estimate`: integer
- `metadata`: object

#### Example validation checks

- reject records with missing `chunk_id`
- reject records where `token_estimate` is not an integer
- reject records where `text` is empty or not a string
- reject records with unsupported `artifact_version`

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

#### Example validation checks

- reject records with missing `embedding`
- reject records where `embedding` is not a list
- reject records where any embedding element is non-numeric
- reject records where vector sizes differ across rows
- reject records with unsupported `artifact_version`

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

---

## Supported artifact versions

Initial supported version set:

- `"1.0"`

If a file contains an unsupported `artifact_version`, `researchAI` should fail with a clear message such as:

```text
Unsupported artifact_version in chunks.jsonl: 2.0
Expected one of: 1.0
```

---

## Failure behavior

Validation failures should be treated as **fatal load-time errors**.

`researchAI` should not continue into retrieval if:

- artifact files are malformed
- required fields are missing
- field types are invalid
- artifact versions are unsupported
- references are inconsistent

This avoids silent corruption and hard-to-debug runtime errors.

---

## Design intent

The purpose of runtime validation is to make the boundary between `dataset-builder` and `researchAI` explicit and reliable.

`dataset-builder` is free to evolve, but any schema change must be reflected by:

1. updating `ARTIFACT_SCHEMA.md`
2. versioning artifacts appropriately
3. updating `researchAI` loaders/validators
