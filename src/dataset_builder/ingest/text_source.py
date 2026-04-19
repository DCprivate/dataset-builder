from __future__ import annotations

from pathlib import Path

from dataset_builder.ingest.base import BaseIngester
from dataset_builder.models import NormalizedDocument
from dataset_builder.utils import normalize_whitespace, sha256_text, title_from_path


class TextIngester(BaseIngester):
    def ingest(self, value: str) -> NormalizedDocument:
        path = Path(value)
        text = path.read_text(encoding="utf-8", errors="ignore")
        normalized = normalize_whitespace(text)
        doc_id = sha256_text(f"text::{value}::{normalized[:4000]}")
        return NormalizedDocument(
            doc_id=doc_id,
            source_type="text",
            source_uri=str(path),
            title=title_from_path(path),
            text=normalized,
            metadata={"path": str(path)},
        )
