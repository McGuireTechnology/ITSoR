from __future__ import annotations

from dataclasses import dataclass, field

import ulid

from itsor.domain.ids import AppId, ColumnId, SliceId, TableId


@dataclass
class Slice:
	id: SliceId = field(default_factory=lambda: SliceId(str(ulid.new())), init=False)
	app_id: AppId
	name: str
	table_id: TableId
	row_filter_expression: str | None = None
	column_list: list[ColumnId] = field(default_factory=list)

	def __post_init__(self) -> None:
		if not self.name.strip():
			raise ValueError("Slice name cannot be empty")


__all__ = ["Slice"]