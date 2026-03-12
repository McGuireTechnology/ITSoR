from abc import ABC, abstractmethod
from typing import Any

from itsor.application.ports.inbox.base_repository import BaseRepository


class OscalDocumentRepository(BaseRepository[Any], ABC):
    @abstractmethod
    def list_by_document_type(self, document_type: str) -> list[Any]: ...
