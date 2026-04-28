import json
from pathlib import Path
#from dataset_builder.models import NormalizedDocument
#from dataset_builder.utils import sha256_text

from dataset_builder.registry import ingest_source
from dataset_builder.ingest.text import TextIngester
from dataset_builder.ingest.pdf import PdfIngester
from dataset_builder.ingest.web import WebsiteIngester
from dataset_builder.ingest.youtube import YouTubeIngester

def load_sources(json_path: str) -> list[dict]:
    path = Path(json_path)

    if not path.exists():
        raise FileNotFoundError(f"Sources file not found: {json_path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Sources file must contain a JSON list")

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Source at index {i} must be an object")

        if "kind" not in item or "value" not in item:
            raise ValueError(f"Source at index {i} must contain 'kind' and 'value'")

        if not isinstance(item["kind"], str) or not isinstance(item["value"], str):
            raise ValueError(f"'kind' and 'value' must be strings at index {i}")

    return data


def build_documents(sources):
    documents = []

    for kind, value in ((source["kind"], source["value"]) for source in sources):
        try:
            doc = ingest_source(kind, value)
            documents.append(doc)
        except Exception as exc:
            print(f"[ERROR] {kind} -> {value}")
            print(f"        {exc}")

    return documents


def main():
    sources = load_sources("../config/sources.json")
    documents = build_documents(sources)

    for doc in documents:
        print("=" * 80)
        print(f"doc_id:       {doc.doc_id}")
        print(f"type:         {doc.source_type}")
        print(f"source:       {doc.source_uri}")
        print(f"title:        {doc.title}")
        print(f"text preview: {doc.text[:50]}")
        print(f"metadata:     {str(doc.metadata)[:50]}")


if __name__ == "__main__":
    main()