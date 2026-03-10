from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TypeAlias

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids import AppId, BotId, EventId, ProcessId, TableId, TaskId


class ResourceAutomationTriggerType(str, Enum):
	ROW_CREATED = "row_created"
	ROW_UPDATED = "row_updated"
	ROW_DELETED = "row_deleted"
	SCHEDULED = "scheduled"


class ResourceAutomationTaskType(str, Enum):
	SEND_EMAIL = "send_email"
	CALL_WEBHOOK = "call_webhook"
	SET_COLUMN_VALUE = "set_column_value"
	CREATE_ROW = "create_row"


ResourceAutomationTaskScalar: TypeAlias = str | int | float | bool | None
ResourceAutomationTaskValue: TypeAlias = (
	ResourceAutomationTaskScalar
	| list[ResourceAutomationTaskScalar]
	| dict[str, ResourceAutomationTaskScalar]
)


def _task_config_factory() -> dict[str, ResourceAutomationTaskValue]:
	return {}


@dataclass
class ResourceAutomationBot:
	id: BotId = field(default_factory=typed_ulid_factory(BotId), init=False)
	app_id: AppId
	name: str
	enabled: bool = True

	def __post_init__(self) -> None:
		self.name = self.name.strip()
		if not self.name:
			raise ValueError("Bot name cannot be empty")


@dataclass
class ResourceAutomationEvent:
	id: EventId = field(default_factory=typed_ulid_factory(EventId), init=False)
	bot_id: BotId
	table_id: TableId | None
	trigger_type: ResourceAutomationTriggerType
	condition_expression: str | None = None

	def __post_init__(self) -> None:
		if self.trigger_type == ResourceAutomationTriggerType.SCHEDULED and self.table_id is not None:
			raise ValueError("Scheduled events must not reference table_id")

		if self.trigger_type != ResourceAutomationTriggerType.SCHEDULED and self.table_id is None:
			raise ValueError("Row events require table_id")


@dataclass
class ResourceAutomationProcess:
	id: ProcessId = field(default_factory=typed_ulid_factory(ProcessId), init=False)
	bot_id: BotId
	name: str

	def __post_init__(self) -> None:
		self.name = self.name.strip()
		if not self.name:
			raise ValueError("Process name cannot be empty")


@dataclass
class ResourceAutomationTask:
	id: TaskId = field(default_factory=typed_ulid_factory(TaskId), init=False)
	process_id: ProcessId
	type: ResourceAutomationTaskType
	config_json: dict[str, ResourceAutomationTaskValue] = field(default_factory=_task_config_factory)


Bot = ResourceAutomationBot
Event = ResourceAutomationEvent
Process = ResourceAutomationProcess
Task = ResourceAutomationTask
TriggerType = ResourceAutomationTriggerType
TaskType = ResourceAutomationTaskType
TaskScalar = ResourceAutomationTaskScalar
TaskValue = ResourceAutomationTaskValue


__all__ = [
	"Bot",
	"Event",
	"Process",
	"ResourceAutomationBot",
	"ResourceAutomationEvent",
	"ResourceAutomationProcess",
	"ResourceAutomationTask",
	"ResourceAutomationTaskScalar",
	"ResourceAutomationTaskType",
	"ResourceAutomationTaskValue",
	"ResourceAutomationTriggerType",
	"Task",
	"TaskScalar",
	"TaskType",
	"TaskValue",
	"TriggerType",
]
