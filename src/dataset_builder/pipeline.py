from dataset_builder.registry import ingest_source
from dataset_builder.chunking import Chunker


def build_documents(sources: list[dict]):
    documents = []
    failures = []

    for kind, value in ((source["kind"], source["value"]) for source in sources):
        try:
            doc = ingest_source(kind, value) # failing here
            documents.append(doc)
        except Exception as exc:
            failures.append({
                "kind": kind,
                "value": value,
                "error": str(exc),
            })

    return documents, failures


def build_chunks(documents, chunker=None):
    chunker = chunker or Chunker()
    chunks = []

    for doc in documents:
        chunks.extend(chunker.chunk_document(doc))

    return chunks