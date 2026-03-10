from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids import AppId, ColumnId, SecurityRuleId, SliceId, TableId


def _column_id_list_factory() -> list[ColumnId]:
	return []


class ResourceAttributeType(str, Enum):
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
class Table:
	id: TableId = field(default_factory=typed_ulid_factory(TableId), init=False)
	app_id: AppId
	name: str
	data_source_id: str | None = None
	primary_key: ColumnId | None = None
	label_column: ColumnId | None = None

	def __post_init__(self) -> None:
		self.name = self.name.strip()
		if not self.name:
			raise ValueError("Table name cannot be empty")


@dataclass
class ResourceAttribute:
	id: ColumnId = field(default_factory=typed_ulid_factory(ColumnId), init=False)
	table_id: TableId
	name: str
	type: ResourceAttributeType
	is_key: bool = False
	is_label: bool = False
	is_required: bool = False
	is_virtual: bool = False
	formula: str | None = None
	ref_table_id: TableId | None = None

	def __post_init__(self) -> None:
		self.name = self.name.strip()
		if not self.name:
			raise ValueError("Column name cannot be empty")

		if self.type == ResourceAttributeType.REF and self.ref_table_id is None:
			raise ValueError("Ref columns require ref_table_id")

		if self.ref_table_id is not None and self.type != ResourceAttributeType.REF:
			raise ValueError("ref_table_id is only valid for ref columns")

		if self.is_virtual and not self.formula:
			raise ValueError("Virtual columns require a formula")


@dataclass
class ResourceSlice:
	id: SliceId = field(default_factory=typed_ulid_factory(SliceId), init=False)
	app_id: AppId
	name: str
	table_id: TableId
	row_filter_expression: str | None = None
	column_list: list[ColumnId] = field(default_factory=_column_id_list_factory)

	def __post_init__(self) -> None:
		self.name = self.name.strip()
		if not self.name:
			raise ValueError("Slice name cannot be empty")


@dataclass
class ResourceSecurityRule:
	id: SecurityRuleId = field(default_factory=typed_ulid_factory(SecurityRuleId), init=False)
	table_id: TableId
	filter_expression: str

	def __post_init__(self) -> None:
		self.filter_expression = self.filter_expression.strip()
		if not self.filter_expression:
			raise ValueError("SecurityRule filter_expression cannot be empty")


Slice = ResourceSlice
Column = ResourceAttribute
ColumnType = ResourceAttributeType
SecurityRule = ResourceSecurityRule


__all__ = [
	"Column",
	"ColumnType",
	"ResourceAttribute",
	"ResourceAttributeType",
	"ResourceSecurityRule",
	"ResourceSlice",
	"SecurityRule",
	"Slice",
	"Table",
]
