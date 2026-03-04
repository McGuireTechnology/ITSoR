import os
from sqlite3 import Connection as SQLiteConnection
from sqlalchemy import create_engine, inspect, text
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from itsor.infrastructure.persistence_models import sqlalchemy_entity_record_model as entity_record_models  # noqa: F401
from itsor.infrastructure.persistence_models import sqlalchemy_entity_type_model as entity_type_models  # noqa: F401
from itsor.infrastructure.persistence_models import sqlalchemy_group_model as group_models  # noqa: F401
from itsor.infrastructure.persistence_models import sqlalchemy_platform_group_membership_model as platform_group_membership_models  # noqa: F401
from itsor.infrastructure.persistence_models import sqlalchemy_idm_group_membership_model as idm_group_membership_models  # noqa: F401
from itsor.infrastructure.persistence_models import sqlalchemy_idm_group_model as idm_group_models  # noqa: F401
from itsor.infrastructure.persistence_models import sqlalchemy_idm_identity_model as idm_identity_models  # noqa: F401
from itsor.infrastructure.persistence_models import sqlalchemy_idm_person_model as idm_person_models  # noqa: F401
from itsor.infrastructure.persistence_models import sqlalchemy_idm_user_model as idm_user_models  # noqa: F401
from itsor.infrastructure.persistence_models import sqlalchemy_namespace_model as namespace_models  # noqa: F401
from itsor.infrastructure.persistence_models import sqlalchemy_platform_endpoint_permission_model as platform_endpoint_permission_models  # noqa: F401
from itsor.infrastructure.persistence_models import sqlalchemy_tenant_model as tenant_models  # noqa: F401
from itsor.infrastructure.persistence_models import sqlalchemy_platform_rbac_models as platform_rbac_models  # noqa: F401
from itsor.infrastructure.persistence_models import sqlalchemy_workspace_model as workspace_models  # noqa: F401
from itsor.infrastructure.persistence_models.sqlalchemy_user_model import Base

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


def _migrate_legacy_platform_tables() -> None:
    table_renames = [
        ("users", "platform_users"),
        ("groups", "platform_groups"),
        ("tenants", "platform_tenants"),
    ]

    existing_tables = set(inspect(engine).get_table_names())
    with engine.begin() as connection:
        for old_name, new_name in table_renames:
            if old_name in existing_tables and new_name not in existing_tables:
                connection.execute(text(f'ALTER TABLE "{old_name}" RENAME TO "{new_name}"'))
                existing_tables.remove(old_name)
                existing_tables.add(new_name)


def create_tables() -> None:
    _migrate_legacy_platform_tables()
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
