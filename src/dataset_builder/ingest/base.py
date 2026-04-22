from abc import ABC, abstractmethod

from ..models import NormalizedDocument

class BaseIngester(ABC):
    @abstractmethod
    def ingest(self, value: str) -> NormalizedDocument:
        raise NotImplementedError