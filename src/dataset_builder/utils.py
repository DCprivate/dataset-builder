import hashlib
import re
from pathlib import Path

def sha256_text(text: str) -> str:
    """ Takes a string and returns a stable hash"""
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def normalize_whitespace(text: str) -> str:
    """Cleans text into a more consistent form"""
    text = text.replace("\r\n", "\n").replace("\r", "\n") # Normalizes line endings
    text = re.sub(r"[ \t]+", " ", text) # Collapses repeated spaces/tabs
    text = re.sub(r"\n{3,}", "\n\n", text) # Collapses excessive blank lines
    return text.strip() # Trims ends


def title_from_path(path: str | Path) -> str:
    return Path(path).stem.replace("_", " ").replace("-", " ").strip()