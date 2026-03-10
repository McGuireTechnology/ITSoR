from typing import NewType

ModuleId = NewType("ModuleId", str)
TableId = NewType("TableId", str)
ColumnId = NewType("ColumnId", str)
RowId = NewType("RowId", str)
ViewId = NewType("ViewId", str)
SliceId = NewType("SliceId", str)
ActionId = NewType("ActionId", str)
BotId = NewType("BotId", str)
EventId = NewType("EventId", str)
ProcessId = NewType("ProcessId", str)
TaskId = NewType("TaskId", str)
AppUserId = NewType("AppUserId", str)
SecurityRuleId = NewType("SecurityRuleId", str)

__all__ = [
	"ActionId",
	"AppUserId",
	"BotId",
	"ColumnId",
	"EventId",
	"ModuleId",
	"ProcessId",
	"RowId",
	"SecurityRuleId",
	"SliceId",
	"TableId",
	"TaskId",
	"ViewId",
]



