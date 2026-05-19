from dataclasses import dataclass, field
from typing import Any


@dataclass
class NormalizedDocument:
    artifact_version: str
    doc_id: str
    source_type: str
    source_uri: str
    title: str | None
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)
    

@dataclass
class ChunkRecord:
    artifact_version: str
    chunk_id: str
    doc_id: str
    text: str
    token_estimate: int
    metadata: dict[str, Any] = field(default_factory=dict)

    #def to_dict(self) -> dict[str, Any]:
    #    return asdict(self)


@dataclass
class ChunkEmbedding:
    artifact_version: str
    chunk_id: str
    doc_id: str
    #text: str
    embedding: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)
