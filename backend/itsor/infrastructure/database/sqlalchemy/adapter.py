from sqlalchemy import inspect, text

from itsor.infrastructure.database.sqlalchemy.connection import engine
from itsor.infrastructure.database.sqlalchemy.models import Base


def create_tables() -> None:
	Base.metadata.create_all(bind=engine)


__all__ = ["create_tables"]
