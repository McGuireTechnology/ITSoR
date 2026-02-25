from abc import abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from itsor.infrastructure.adapters.base_repository import BaseRepository


TEntity = TypeVar("TEntity")
TModel = TypeVar("TModel")


class SQLAlchemyBaseRepository(BaseRepository[TEntity], Generic[TEntity, TModel]):
    model_class: type[TModel]

    def __init__(self, db: Session, entity_label: str) -> None:
        super().__init__(entity_label)
        self._db = db

    @abstractmethod
    def _to_domain(self, record: TModel) -> TEntity:
        ...

    @abstractmethod
    def _to_model(self, entity: TEntity) -> TModel:
        ...

    @abstractmethod
    def _apply_updates(self, record: TModel, entity: TEntity) -> None:
        ...

    def get_by_id(self, entity_id: str) -> TEntity | None:
        record = self._db.query(self.model_class).filter(self.model_class.id == entity_id).first()
        return self._to_domain(record) if record else None

    def list(self) -> list[TEntity]:
        records = self._db.query(self.model_class).all()
        return [self._to_domain(record) for record in records]

    def create(self, entity: TEntity) -> TEntity:
        record = self._to_model(entity)
        self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return self._to_domain(record)

    def update(self, entity: TEntity) -> TEntity:
        entity_id = getattr(entity, "id")
        record = self._db.query(self.model_class).filter(self.model_class.id == entity_id).first()
        if not record:
            raise ValueError(self._not_found_message(entity_id))
        self._apply_updates(record, entity)
        self._db.commit()
        self._db.refresh(record)
        return self._to_domain(record)

    def delete(self, entity_id: str) -> None:
        record = self._db.query(self.model_class).filter(self.model_class.id == entity_id).first()
        if record:
            self._db.delete(record)
            self._db.commit()
