from __future__ import annotations

from dataclasses import dataclass, field

import ulid

from itsor.domain.ids import AppId, ColumnId, TableId


@dataclass
class Table:
	id: TableId = field(default_factory=lambda: TableId(str(ulid.new())), init=False)
	app_id: AppId
	name: str
	data_source_id: str | None = None
	primary_key: ColumnId | None = None
	label_column: ColumnId | None = None

	def __post_init__(self) -> None:
		if not self.name.strip():
			raise ValueError("Table name cannot be empty")


__all__ = ["Table"]