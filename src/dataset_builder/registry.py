from dataset_builder.ingest.pdf import PdfIngester
from dataset_builder.ingest.text import TextIngester
from dataset_builder.ingest.web import WebsiteIngester
from dataset_builder.ingest.youtube import YouTubeIngester

INGESTER_REGISTRY = {
    "text": TextIngester,
    "pdf": PdfIngester,
    "website": WebsiteIngester,
    "youtube": YouTubeIngester,
}

def ingest_source(kind: str, value: str):
    ingester_cls = INGESTER_REGISTRY.get(kind)
    if not ingester_cls:
        raise ValueError(f"Unsupported source type: {kind}")
    return ingester_cls().ingest(value)