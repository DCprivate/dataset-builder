import trafilatura

from dataset_builder.ingest.base import BaseIngester
from dataset_builder.models import NormalizedDocument
from dataset_builder.utils import normalize_whitespace, sha256_text


class WebsiteIngester(BaseIngester):
    def ingest(self, value: str) -> NormalizedDocument:
        downloaded = trafilatura.fetch_url(value)
        if not downloaded:
            raise ValueError(f"Failed to download website content: {value}")

        metadata = trafilatura.extract_metadata(downloaded)

        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=True,
            include_images=False,
            favor_precision=True,
        )

        if not text:
            raise ValueError(f"No extractable text found for website: {value}")

        normalized = normalize_whitespace(text)
        title = metadata.title if metadata and metadata.title else None
        doc_id = sha256_text(f"website::{value}::{normalized[:4000]}")

        return NormalizedDocument(
            doc_id=doc_id,
            source_type="website",
            source_uri=value,
            title=title,
            text=normalized,
            metadata={
                "url": value,
                "hostname": metadata.hostname if metadata and metadata.hostname else None,
                "date": metadata.date if metadata and metadata.date else None,
                "author": metadata.author if metadata and metadata.author else None,
            },
        )