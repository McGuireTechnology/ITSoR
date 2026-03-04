from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar


TModel = TypeVar("TModel")


class BaseRepository(ABC, Generic[TModel]):
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[TModel]:
        ...

    @abstractmethod
    def list(self) -> List[TModel]:
        ...

    @abstractmethod
    def create(self, entity: TModel) -> TModel:
        ...

    @abstractmethod
    def update(self, entity: TModel) -> TModel:
        ...

    @abstractmethod
    def delete(self, entity_id: str) -> None:
        ...
