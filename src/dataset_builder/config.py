from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field


SourceKind = Literal["website", "pdf", "text", "youtube"]


class SourceSpec(BaseModel):
    kind: SourceKind
    value: str


class ChunkingConfig(BaseModel):
    chunk_size: int = Field(default=900, ge=100)
    chunk_overlap: int = Field(default=150, ge=0)
    min_chunk_chars: int = Field(default=200, ge=1)


class BuildConfig(BaseModel):
    chunking: ChunkingConfig = ChunkingConfig()
    sources: list[SourceSpec] = []


def load_config(path: str | Path) -> BuildConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return BuildConfig.model_validate(data)
