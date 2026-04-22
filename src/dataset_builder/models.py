from dataclasses import dataclass, field
from typing import Any

@dataclass
class NormalizedDocument:
    doc_id: str
    source_type: str
    source_url: str
    title: str | None
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)