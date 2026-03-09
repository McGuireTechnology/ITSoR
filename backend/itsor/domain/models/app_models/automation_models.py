from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TypeAlias

import ulid

from itsor.domain.ids import AppId, BotId, EventId, ProcessId, TableId, TaskId

TaskScalar: TypeAlias = str | int | float | bool | None
TaskValue: TypeAlias = TaskScalar | list[TaskScalar] | dict[str, TaskScalar]


class TriggerType(str, Enum):
	ROW_CREATED = "row_created"
	ROW_UPDATED = "row_updated"
	ROW_DELETED = "row_deleted"
	SCHEDULED = "scheduled"


class TaskType(str, Enum):
	SEND_EMAIL = "send_email"
	CALL_WEBHOOK = "call_webhook"
	SET_COLUMN_VALUE = "set_column_value"
	CREATE_ROW = "create_row"


@dataclass
class Bot:
	id: BotId = field(default_factory=lambda: BotId(str(ulid.new())), init=False)
	app_id: AppId
	name: str
	enabled: bool = True

	def __post_init__(self) -> None:
		if not self.name.strip():
			raise ValueError("Bot name cannot be empty")


@dataclass
class Event:
	id: EventId = field(default_factory=lambda: EventId(str(ulid.new())), init=False)
	bot_id: BotId
	table_id: TableId | None
	trigger_type: TriggerType
	condition_expression: str | None = None

	def __post_init__(self) -> None:
		if self.trigger_type == TriggerType.SCHEDULED and self.table_id is not None:
			raise ValueError("Scheduled events must not reference table_id")

		if self.trigger_type != TriggerType.SCHEDULED and self.table_id is None:
			raise ValueError("Row events require table_id")


@dataclass
class Process:
	id: ProcessId = field(default_factory=lambda: ProcessId(str(ulid.new())), init=False)
	bot_id: BotId
	name: str

	def __post_init__(self) -> None:
		if not self.name.strip():
			raise ValueError("Process name cannot be empty")


@dataclass
class Task:
	id: TaskId = field(default_factory=lambda: TaskId(str(ulid.new())), init=False)
	process_id: ProcessId
	type: TaskType
	config_json: dict[str, TaskValue] = field(default_factory=dict)


__all__ = [
	"Bot",
	"Event",
	"Process",
	"Task",
	"TaskScalar",
	"TaskType",
	"TaskValue",
	"TriggerType",
]