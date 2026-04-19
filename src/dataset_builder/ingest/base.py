from __future__ import annotations

from abc import ABC, abstractmethod

from dataset_builder.models import NormalizedDocument


class BaseIngester(ABC):
    @abstractmethod
    def ingest(self, value: str) -> NormalizedDocument:
        raise NotImplementedError
