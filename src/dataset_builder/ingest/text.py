from pathlib import Path

from dataset_builder.schema import ARTIFACT_VERSION
from dataset_builder.ingest.base import BaseIngester
from dataset_builder.models import NormalizedDocument
from dataset_builder.utils import sha256_text, normalize_whitespace, title_from_path


class TextIngester(BaseIngester):
    
    def ingest(self, value: str) -> NormalizedDocument:
        path = Path(value)
        text = path.read_text(encoding="utf-8", errors="ignore") # TODO: Remember to change from "ignore" for stricter handling
        normalized = normalize_whitespace(text)

        doc_id = sha256_text(f"text::{value}::{normalized[:4000]}") # Hash depends on content without hashing arbitrarily large strings in the id seed
        
        return NormalizedDocument(
            artifact_version=ARTIFACT_VERSION,            
            doc_id=doc_id,
            source_type="text",
            source_uri=str(path),
            title=title_from_path(path), # TODO: Probably going to need to clean up paths to not include //
            text=normalized,
            metadata={"path": str(path)},
        )