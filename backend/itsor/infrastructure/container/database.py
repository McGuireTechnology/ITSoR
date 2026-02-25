import os
from sqlite3 import Connection as SQLiteConnection
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from itsor.infrastructure.models import sqlalchemy_entity_record_model as entity_record_models  # noqa: F401
from itsor.infrastructure.models import sqlalchemy_entity_type_model as entity_type_models  # noqa: F401
from itsor.infrastructure.models import sqlalchemy_group_model as group_models  # noqa: F401
from itsor.infrastructure.models import sqlalchemy_namespace_model as namespace_models  # noqa: F401
from itsor.infrastructure.models import sqlalchemy_tenant_model as tenant_models  # noqa: F401
from itsor.infrastructure.models import sqlalchemy_workspace_model as workspace_models  # noqa: F401
from itsor.infrastructure.models.sqlalchemy_user_model import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./itsor.db")

engine = create_engine(
    DATABASE_URL,
    connect_args=(
        {"check_same_thread": False, "timeout": 30}
        if DATABASE_URL.startswith("sqlite")
        else {}
    ),
)

if DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def _set_sqlite_pragmas(dbapi_connection, _connection_record):
        if isinstance(dbapi_connection, SQLiteConnection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
