from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids import ActionId, AppId, TableId


class ResourceActionType(str, Enum):
	SET_COLUMN_VALUE = "set_column_value"
	ADD_ROW = "add_row"
	DELETE_ROW = "delete_row"
	NAVIGATE = "navigate"
	CALL_WEBHOOK = "call_webhook"


@dataclass
class ResourceAction:
	id: ActionId = field(default_factory=typed_ulid_factory(ActionId), init=False)
	app_id: AppId
	name: str
	table_id: TableId
	type: ResourceActionType
	condition_expression: str | None = None
	target_expression: str | None = None

	def __post_init__(self) -> None:
		self.name = self.name.strip()
		if not self.name:
			raise ValueError("Action name cannot be empty")


Action = ResourceAction
ActionType = ResourceActionType


__all__ = ["Action", "ActionType", "ResourceAction", "ResourceActionType"]
