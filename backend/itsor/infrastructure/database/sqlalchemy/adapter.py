from sqlalchemy import inspect, text

from itsor.infrastructure.database.sqlalchemy.connection import engine
from itsor.infrastructure.database.sqlalchemy.models import Base


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


__all__ = ["create_tables"]
