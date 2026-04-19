from __future__ import annotations

from importlib import import_module

INGESTER_REGISTRY = {
    "website": "dataset_builder.ingest.web:WebsiteIngester",
    "pdf": "dataset_builder.ingest.pdf:PdfIngester",
    "text": "dataset_builder.ingest.text_source:TextIngester",
    "youtube": "dataset_builder.ingest.youtube:YouTubeIngester",
}


def resolve_ingester(kind: str):
    target = INGESTER_REGISTRY.get(kind)
    if not target:
        raise ValueError(f"No ingester registered for source kind: {kind}")
    module_name, class_name = target.split(":", 1)
    module = import_module(module_name)
    return getattr(module, class_name)
