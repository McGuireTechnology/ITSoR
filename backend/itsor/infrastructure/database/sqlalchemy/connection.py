import os
from sqlite3 import Connection as SQLiteConnection
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

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


def get_db() -> Generator[Session, None, None]:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


__all__ = ["DATABASE_URL", "engine", "SessionLocal", "get_db"]
