from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import ulid

from itsor.domain.ids import ActionId, AppId, TableId


class ActionType(str, Enum):
	SET_COLUMN_VALUE = "set_column_value"
	ADD_ROW = "add_row"
	DELETE_ROW = "delete_row"
	NAVIGATE = "navigate"
	CALL_WEBHOOK = "call_webhook"


@dataclass
class Action:
	id: ActionId = field(default_factory=lambda: ActionId(str(ulid.new())), init=False)
	app_id: AppId
	name: str
	table_id: TableId
	type: ActionType
	condition_expression: str | None = None
	target_expression: str | None = None

	def __post_init__(self) -> None:
		if not self.name.strip():
			raise ValueError("Action name cannot be empty")


__all__ = ["Action", "ActionType"]