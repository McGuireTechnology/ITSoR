from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import ulid

from itsor.domain.ids import ColumnId, TableId


class ColumnType(str, Enum):
	TEXT = "text"
	NUMBER = "number"
	BOOLEAN = "boolean"
	DATE = "date"
	ENUM = "enum"
	REF = "ref"
	FILE = "file"
	IMAGE = "image"
	LOCATION = "location"


@dataclass
class Column:
	id: ColumnId = field(default_factory=lambda: ColumnId(str(ulid.new())), init=False)
	table_id: TableId
	name: str
	type: ColumnType
	is_key: bool = False
	is_label: bool = False
	is_required: bool = False
	is_virtual: bool = False
	formula: str | None = None
	ref_table_id: TableId | None = None

	def __post_init__(self) -> None:
		if not self.name.strip():
			raise ValueError("Column name cannot be empty")

		if self.type == ColumnType.REF and self.ref_table_id is None:
			raise ValueError("Ref columns require ref_table_id")

		if self.ref_table_id is not None and self.type != ColumnType.REF:
			raise ValueError("ref_table_id is only valid for ref columns")

		if self.is_virtual and not self.formula:
			raise ValueError("Virtual columns require a formula")


__all__ = ["Column", "ColumnType"]