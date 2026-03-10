from typing import NewType

from itsor.domain.ids.module_ids import (
	ActionId,
	AppUserId,
	BotId,
	ColumnId,
	EventId,
	ProcessId,
	RowId,
	SecurityRuleId,
	SliceId,
	TableId,
	TaskId,
	ViewId,
)

AppId = NewType("AppId", str)

__all__ = [
	"ActionId",
	"AppId",
	"AppUserId",
	"BotId",
	"ColumnId",
	"EventId",
	"ProcessId",
	"RowId",
	"SecurityRuleId",
	"SliceId",
	"TableId",
	"TaskId",
	"ViewId",
]
