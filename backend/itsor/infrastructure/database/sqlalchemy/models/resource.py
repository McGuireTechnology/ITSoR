import ulid
from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.dialects.postgresql import JSONB

from itsor.infrastructure.database.sqlalchemy.models.auth import Base


class TableModel(Base):
    __tablename__ = "resource_tables"

    id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
    app_id = Column(String(36), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    data_source_id = Column(String(36), nullable=True, index=True)
    primary_key = Column(String(36), nullable=True, index=True)
    label_column = Column(String(36), nullable=True, index=True)


class ResourceAttributeModel(Base):
    __tablename__ = "resource_attributes"
    __table_args__ = (
        CheckConstraint(
            "type in ('text', 'number', 'boolean', 'date', 'enum', 'ref', 'file', 'image', 'location')",
            name="ck_resource_attributes_type",
        ),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
    table_id = Column(String(36), ForeignKey("resource_tables.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    type = Column(String(32), nullable=False, index=True)
    is_key = Column(Boolean, nullable=False, default=False)
    is_label = Column(Boolean, nullable=False, default=False)
    is_required = Column(Boolean, nullable=False, default=False)
    is_virtual = Column(Boolean, nullable=False, default=False)
    formula = Column(String(2048), nullable=True)
    ref_table_id = Column(String(36), ForeignKey("resource_tables.id"), nullable=True, index=True)


class ResourceSliceModel(Base):
    __tablename__ = "resource_slices"

    id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
    app_id = Column(String(36), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    table_id = Column(String(36), ForeignKey("resource_tables.id"), nullable=False, index=True)
    row_filter_expression = Column(String(2048), nullable=True)
    column_list_json = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=list)


class ResourceSecurityRuleModel(Base):
    __tablename__ = "resource_security_rules"

    id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
    table_id = Column(String(36), ForeignKey("resource_tables.id"), nullable=False, index=True)
    filter_expression = Column(String(2048), nullable=False)


class ResourceRecordModel(Base):
    __tablename__ = "resource_records"

    id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
    table_id = Column(String(36), ForeignKey("resource_tables.id"), nullable=False, index=True)
    data_json = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)
    created_at = Column(DateTime, nullable=False, index=True)
    updated_at = Column(DateTime, nullable=False, index=True)


class ResourceActionModel(Base):
    __tablename__ = "resource_actions"
    __table_args__ = (
        CheckConstraint(
            "type in ('set_column_value', 'add_row', 'delete_row', 'navigate', 'call_webhook')",
            name="ck_resource_actions_type",
        ),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
    app_id = Column(String(36), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    table_id = Column(String(36), ForeignKey("resource_tables.id"), nullable=False, index=True)
    type = Column(String(32), nullable=False, index=True)
    condition_expression = Column(String(2048), nullable=True)
    target_expression = Column(String(2048), nullable=True)


class ResourceAutomationBotModel(Base):
    __tablename__ = "resource_automation_bots"

    id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
    app_id = Column(String(36), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    enabled = Column(Boolean, nullable=False, default=True)


class ResourceAutomationEventModel(Base):
    __tablename__ = "resource_automation_events"
    __table_args__ = (
        CheckConstraint(
            "trigger_type in ('row_created', 'row_updated', 'row_deleted', 'scheduled')",
            name="ck_resource_automation_events_trigger_type",
        ),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
    bot_id = Column(String(36), ForeignKey("resource_automation_bots.id"), nullable=False, index=True)
    table_id = Column(String(36), ForeignKey("resource_tables.id"), nullable=True, index=True)
    trigger_type = Column(String(32), nullable=False, index=True)
    condition_expression = Column(String(2048), nullable=True)


class ResourceAutomationProcessModel(Base):
    __tablename__ = "resource_automation_processes"

    id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
    bot_id = Column(String(36), ForeignKey("resource_automation_bots.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)


class ResourceAutomationTaskModel(Base):
    __tablename__ = "resource_automation_tasks"
    __table_args__ = (
        CheckConstraint(
            "type in ('send_email', 'call_webhook', 'set_column_value', 'create_row')",
            name="ck_resource_automation_tasks_type",
        ),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
    process_id = Column(String(36), ForeignKey("resource_automation_processes.id"), nullable=False, index=True)
    type = Column(String(32), nullable=False, index=True)
    config_json = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)


ColumnModel = ResourceAttributeModel
SliceModel = ResourceSliceModel
SecurityRuleModel = ResourceSecurityRuleModel
RowModel = ResourceRecordModel
ActionModel = ResourceActionModel
BotModel = ResourceAutomationBotModel
EventModel = ResourceAutomationEventModel
ProcessModel = ResourceAutomationProcessModel
TaskModel = ResourceAutomationTaskModel


__all__ = [
    "ActionModel",
    "BotModel",
    "ColumnModel",
    "EventModel",
    "ProcessModel",
    "ResourceActionModel",
    "ResourceAttributeModel",
    "ResourceAutomationBotModel",
    "ResourceAutomationEventModel",
    "ResourceAutomationProcessModel",
    "ResourceAutomationTaskModel",
    "ResourceRecordModel",
    "ResourceSecurityRuleModel",
    "ResourceSliceModel",
    "RowModel",
    "SecurityRuleModel",
    "SliceModel",
    "TableModel",
    "TaskModel",
]
