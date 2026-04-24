from pathlib import Path
from pypdf import PdfReader

from dataset_builder.ingest.base import BaseIngester
from dataset_builder.models import NormalizedDocument
from dataset_builder.utils import sha256_text, normalize_whitespace, title_from_path

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
                f"No text extracted from PDF: {value}. The PDF may be image-only and need OCR."
            )

        pdf_meta = {str(k): str(v) for k, v in (reader.metadata or {}).items()}

        title = pdf_meta.get("/Title") or title_from_path(path)
        doc_id = sha256_text(f"pdf::{value}::{normalized[:4000]}")

        return NormalizedDocument(
            doc_id=doc_id,
            source_type="pdf",
            source_uri=str(path),
            title=title,
            text=normalized,
            metadata={
                "path": str(path),
                "pages": len(reader.pages),
                "pdf_metadata": pdf_meta,
            },
        )