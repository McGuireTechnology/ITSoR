from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TypeAlias

import ulid

from itsor.domain.ids import RowId, TableId

RowScalar: TypeAlias = str | int | float | bool | None
RowValue: TypeAlias = RowScalar | list[RowScalar]


@dataclass
class Row:
	id: RowId = field(default_factory=lambda: RowId(str(ulid.new())), init=False)
	table_id: TableId
	data_json: dict[str, RowValue] = field(default_factory=dict)
	created_at: datetime = field(default_factory=lambda: datetime.now(UTC), init=False)
	updated_at: datetime = field(default_factory=lambda: datetime.now(UTC), init=False)

	def touch(self) -> None:
		self.updated_at = datetime.now(UTC)


__all__ = ["Row", "RowScalar", "RowValue"]