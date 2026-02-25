from typing import Generic

from itsor.infrastructure.adapters.base_repository import BaseRepository, TEntity


class InMemoryBaseRepository(BaseRepository[TEntity], Generic[TEntity]):
    def __init__(self, entity_label: str) -> None:
        super().__init__(entity_label)
        self._items: dict[str, TEntity] = {}

    def get_by_id(self, entity_id: str) -> TEntity | None:
        return self._items.get(entity_id)

    def list(self) -> list[TEntity]:
        return list(self._items.values())

    def create(self, entity: TEntity) -> TEntity:
        entity_id = getattr(entity, "id")
        self._items[entity_id] = entity
        return entity

    def update(self, entity: TEntity) -> TEntity:
        entity_id = getattr(entity, "id")
        if entity_id not in self._items:
            raise ValueError(self._not_found_message(entity_id))
        self._items[entity_id] = entity
        return entity

    def delete(self, entity_id: str) -> None:
        self._items.pop(entity_id, None)
