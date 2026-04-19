from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Iterable


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def title_from_path(path: str | Path) -> str:
    return Path(path).stem.replace("_", " ").replace("-", " ").strip()


def batched(items: list, size: int) -> Iterable[list]:
    for idx in range(0, len(items), size):
        yield items[idx : idx + size]
