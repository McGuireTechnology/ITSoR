from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TypeAlias

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids import RowId, TableId


ResourceRecordScalar: TypeAlias = str | int | float | bool | None
ResourceRecordValue: TypeAlias = ResourceRecordScalar | list[ResourceRecordScalar]


def _record_data_factory() -> dict[str, ResourceRecordValue]:
	return {}


@dataclass
class ResourceRecord:
	id: RowId = field(default_factory=typed_ulid_factory(RowId), init=False)
	table_id: TableId
	data_json: dict[str, ResourceRecordValue] = field(default_factory=_record_data_factory)
	created_at: datetime = field(default_factory=lambda: datetime.now(UTC), init=False)
	updated_at: datetime = field(default_factory=lambda: datetime.now(UTC), init=False)

	def touch(self) -> None:
		self.updated_at = datetime.now(UTC)


Row = ResourceRecord
RowScalar = ResourceRecordScalar
RowValue = ResourceRecordValue


__all__ = [
	"ResourceRecord",
	"ResourceRecordScalar",
	"ResourceRecordValue",
	"Row",
	"RowScalar",
	"RowValue",
]
