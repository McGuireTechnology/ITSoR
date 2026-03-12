from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


ResourceAttributeTypeLiteral = Literal[
    "text",
    "number",
    "boolean",
    "date",
    "enum",
    "ref",
    "file",
    "image",
    "location",
]
ResourceActionTypeLiteral = Literal[
    "set_column_value",
    "add_row",
    "delete_row",
    "navigate",
    "call_webhook",
]
ResourceAutomationTriggerTypeLiteral = Literal[
    "row_created",
    "row_updated",
    "row_deleted",
    "scheduled",
]
ResourceAutomationTaskTypeLiteral = Literal[
    "send_email",
    "call_webhook",
    "set_column_value",
    "create_row",
]


class TableCreate(BaseModel):
    app_id: str
    name: str
    data_source_id: str | None = None
    primary_key: str | None = None
    label_column: str | None = None


class TableReplace(TableCreate):
    pass


class TableUpdate(BaseModel):
    app_id: str | None = None
    name: str | None = None
    data_source_id: str | None = None
    primary_key: str | None = None
    label_column: str | None = None


class TableResponse(BaseModel):
    id: str
    app_id: str
    name: str
    data_source_id: str | None = None
    primary_key: str | None = None
    label_column: str | None = None

    model_config = {"from_attributes": True}


class ResourceAttributeCreate(BaseModel):
    table_id: str
    name: str
    type: ResourceAttributeTypeLiteral
    is_key: bool = False
    is_label: bool = False
    is_required: bool = False
    is_virtual: bool = False
    formula: str | None = None
    ref_table_id: str | None = None


class ResourceAttributeReplace(ResourceAttributeCreate):
    pass


class ResourceAttributeUpdate(BaseModel):
    table_id: str | None = None
    name: str | None = None
    type: ResourceAttributeTypeLiteral | None = None
    is_key: bool | None = None
    is_label: bool | None = None
    is_required: bool | None = None
    is_virtual: bool | None = None
    formula: str | None = None
    ref_table_id: str | None = None


class ResourceAttributeResponse(BaseModel):
    id: str
    table_id: str
    name: str
    type: ResourceAttributeTypeLiteral
    is_key: bool = False
    is_label: bool = False
    is_required: bool = False
    is_virtual: bool = False
    formula: str | None = None
    ref_table_id: str | None = None

    model_config = {"from_attributes": True}


class ResourceSliceCreate(BaseModel):
    app_id: str
    name: str
    table_id: str
    row_filter_expression: str | None = None
    column_list: list[str] = Field(default_factory=list)


class ResourceSliceReplace(ResourceSliceCreate):
    pass


class ResourceSliceUpdate(BaseModel):
    app_id: str | None = None
    name: str | None = None
    table_id: str | None = None
    row_filter_expression: str | None = None
    column_list: list[str] | None = None


class ResourceSliceResponse(BaseModel):
    id: str
    app_id: str
    name: str
    table_id: str
    row_filter_expression: str | None = None
    column_list: list[str] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class ResourceSecurityRuleCreate(BaseModel):
    table_id: str
    filter_expression: str


class ResourceSecurityRuleReplace(ResourceSecurityRuleCreate):
    pass


class ResourceSecurityRuleUpdate(BaseModel):
    table_id: str | None = None
    filter_expression: str | None = None


class ResourceSecurityRuleResponse(BaseModel):
    id: str
    table_id: str
    filter_expression: str

    model_config = {"from_attributes": True}


class ResourceRecordCreate(BaseModel):
    table_id: str
    data_json: dict[str, Any] = Field(default_factory=dict)


class ResourceRecordReplace(ResourceRecordCreate):
    pass


class ResourceRecordUpdate(BaseModel):
    table_id: str | None = None
    data_json: dict[str, Any] | None = None


class ResourceRecordResponse(BaseModel):
    id: str
    table_id: str
    data_json: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ResourceActionCreate(BaseModel):
    app_id: str
    name: str
    table_id: str
    type: ResourceActionTypeLiteral
    condition_expression: str | None = None
    target_expression: str | None = None


class ResourceActionReplace(ResourceActionCreate):
    pass


class ResourceActionUpdate(BaseModel):
    app_id: str | None = None
    name: str | None = None
    table_id: str | None = None
    type: ResourceActionTypeLiteral | None = None
    condition_expression: str | None = None
    target_expression: str | None = None


class ResourceActionResponse(BaseModel):
    id: str
    app_id: str
    name: str
    table_id: str
    type: ResourceActionTypeLiteral
    condition_expression: str | None = None
    target_expression: str | None = None

    model_config = {"from_attributes": True}


class ResourceAutomationBotCreate(BaseModel):
    app_id: str
    name: str
    enabled: bool = True


class ResourceAutomationBotReplace(ResourceAutomationBotCreate):
    pass


class ResourceAutomationBotUpdate(BaseModel):
    app_id: str | None = None
    name: str | None = None
    enabled: bool | None = None


class ResourceAutomationBotResponse(BaseModel):
    id: str
    app_id: str
    name: str
    enabled: bool = True

    model_config = {"from_attributes": True}


class ResourceAutomationEventCreate(BaseModel):
    bot_id: str
    table_id: str | None = None
    trigger_type: ResourceAutomationTriggerTypeLiteral
    condition_expression: str | None = None


class ResourceAutomationEventReplace(ResourceAutomationEventCreate):
    pass


class ResourceAutomationEventUpdate(BaseModel):
    bot_id: str | None = None
    table_id: str | None = None
    trigger_type: ResourceAutomationTriggerTypeLiteral | None = None
    condition_expression: str | None = None


class ResourceAutomationEventResponse(BaseModel):
    id: str
    bot_id: str
    table_id: str | None = None
    trigger_type: ResourceAutomationTriggerTypeLiteral
    condition_expression: str | None = None

    model_config = {"from_attributes": True}


class ResourceAutomationProcessCreate(BaseModel):
    bot_id: str
    name: str


class ResourceAutomationProcessReplace(ResourceAutomationProcessCreate):
    pass


class ResourceAutomationProcessUpdate(BaseModel):
    bot_id: str | None = None
    name: str | None = None


class ResourceAutomationProcessResponse(BaseModel):
    id: str
    bot_id: str
    name: str

    model_config = {"from_attributes": True}


class ResourceAutomationTaskCreate(BaseModel):
    process_id: str
    type: ResourceAutomationTaskTypeLiteral
    config_json: dict[str, Any] = Field(default_factory=dict)


class ResourceAutomationTaskReplace(ResourceAutomationTaskCreate):
    pass


class ResourceAutomationTaskUpdate(BaseModel):
    process_id: str | None = None
    type: ResourceAutomationTaskTypeLiteral | None = None
    config_json: dict[str, Any] | None = None


class ResourceAutomationTaskResponse(BaseModel):
    id: str
    process_id: str
    type: ResourceAutomationTaskTypeLiteral
    config_json: dict[str, Any] = Field(default_factory=dict)

    model_config = {"from_attributes": True}


ColumnCreate = ResourceAttributeCreate
ColumnReplace = ResourceAttributeReplace
ColumnUpdate = ResourceAttributeUpdate
ColumnResponse = ResourceAttributeResponse
SliceCreate = ResourceSliceCreate
SliceReplace = ResourceSliceReplace
SliceUpdate = ResourceSliceUpdate
SliceResponse = ResourceSliceResponse
SecurityRuleCreate = ResourceSecurityRuleCreate
SecurityRuleReplace = ResourceSecurityRuleReplace
SecurityRuleUpdate = ResourceSecurityRuleUpdate
SecurityRuleResponse = ResourceSecurityRuleResponse
RowCreate = ResourceRecordCreate
RowReplace = ResourceRecordReplace
RowUpdate = ResourceRecordUpdate
RowResponse = ResourceRecordResponse
ActionCreate = ResourceActionCreate
ActionReplace = ResourceActionReplace
ActionUpdate = ResourceActionUpdate
ActionResponse = ResourceActionResponse
BotCreate = ResourceAutomationBotCreate
BotReplace = ResourceAutomationBotReplace
BotUpdate = ResourceAutomationBotUpdate
BotResponse = ResourceAutomationBotResponse
EventCreate = ResourceAutomationEventCreate
EventReplace = ResourceAutomationEventReplace
EventUpdate = ResourceAutomationEventUpdate
EventResponse = ResourceAutomationEventResponse
ProcessCreate = ResourceAutomationProcessCreate
ProcessReplace = ResourceAutomationProcessReplace
ProcessUpdate = ResourceAutomationProcessUpdate
ProcessResponse = ResourceAutomationProcessResponse
TaskCreate = ResourceAutomationTaskCreate
TaskReplace = ResourceAutomationTaskReplace
TaskUpdate = ResourceAutomationTaskUpdate
TaskResponse = ResourceAutomationTaskResponse


__all__ = [
    "ActionCreate",
    "ActionReplace",
    "ActionResponse",
    "ActionUpdate",
    "BotCreate",
    "BotReplace",
    "BotResponse",
    "BotUpdate",
    "ColumnCreate",
    "ColumnReplace",
    "ColumnResponse",
    "ColumnUpdate",
    "EventCreate",
    "EventReplace",
    "EventResponse",
    "EventUpdate",
    "ProcessCreate",
    "ProcessReplace",
    "ProcessResponse",
    "ProcessUpdate",
    "ResourceActionCreate",
    "ResourceActionReplace",
    "ResourceActionResponse",
    "ResourceActionUpdate",
    "ResourceAttributeCreate",
    "ResourceAttributeReplace",
    "ResourceAttributeResponse",
    "ResourceAttributeUpdate",
    "ResourceAutomationBotCreate",
    "ResourceAutomationBotReplace",
    "ResourceAutomationBotResponse",
    "ResourceAutomationBotUpdate",
    "ResourceAutomationEventCreate",
    "ResourceAutomationEventReplace",
    "ResourceAutomationEventResponse",
    "ResourceAutomationEventUpdate",
    "ResourceAutomationProcessCreate",
    "ResourceAutomationProcessReplace",
    "ResourceAutomationProcessResponse",
    "ResourceAutomationProcessUpdate",
    "ResourceAutomationTaskCreate",
    "ResourceAutomationTaskReplace",
    "ResourceAutomationTaskResponse",
    "ResourceAutomationTaskUpdate",
    "ResourceRecordCreate",
    "ResourceRecordReplace",
    "ResourceRecordResponse",
    "ResourceRecordUpdate",
    "ResourceSecurityRuleCreate",
    "ResourceSecurityRuleReplace",
    "ResourceSecurityRuleResponse",
    "ResourceSecurityRuleUpdate",
    "ResourceSliceCreate",
    "ResourceSliceReplace",
    "ResourceSliceResponse",
    "ResourceSliceUpdate",
    "RowCreate",
    "RowReplace",
    "RowResponse",
    "RowUpdate",
    "SecurityRuleCreate",
    "SecurityRuleReplace",
    "SecurityRuleResponse",
    "SecurityRuleUpdate",
    "SliceCreate",
    "SliceReplace",
    "SliceResponse",
    "SliceUpdate",
    "TableCreate",
    "TableReplace",
    "TableResponse",
    "TableUpdate",
    "TaskCreate",
    "TaskReplace",
    "TaskResponse",
    "TaskUpdate",
]
