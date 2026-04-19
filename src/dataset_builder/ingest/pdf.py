from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

from dataset_builder.ingest.base import BaseIngester
from dataset_builder.models import NormalizedDocument
from dataset_builder.utils import normalize_whitespace, sha256_text, title_from_path


class PdfIngester(BaseIngester):
    def ingest(self, value: str) -> NormalizedDocument:
        path = Path(value)
        reader = PdfReader(str(path))

        page_texts: list[str] = []
        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                page_texts.append(f"\n\n[Page {idx + 1}]\n{text}")

        full_text = "".join(page_texts)
        normalized = normalize_whitespace(full_text)
        if not normalized:
            raise ValueError(
                f"No text extracted from PDF: {value}. This may be an image-only PDF and need OCR."
            )

        metadata = {
            "path": str(path),
            "pages": len(reader.pages),
            "pdf_metadata": {str(k): str(v) for k, v in (reader.metadata or {}).items()},
        }
        title = metadata["pdf_metadata"].get("/Title") or title_from_path(path)
        doc_id = sha256_text(f"pdf::{value}::{normalized[:4000]}")

        return NormalizedDocument(
            doc_id=doc_id,
            source_type="pdf",
            source_uri=str(path),
            title=title,
            text=normalized,
            metadata=metadata,
        )
