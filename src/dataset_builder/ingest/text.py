from pathlib import Path

from dataset_builder.ingest.base import BaseIngester
from dataset_builder.models import NormalizedDocument
from dataset_builder.utils import sha256_text, normalize_whitespace, title_from_path

class TextIngester(BaseIngester):
    
    def ingest(self, value: str) -> NormalizedDocument:
        print("Ingesting", value)