# Resource Automation Models

Source: `backend/itsor/domain/models/resource_models/automation_models.py`

---

## Purpose

Defines automation entities (bot, event, process, task) used to execute rule-driven operations over resource data.

## Models

- **ResourceAutomationBot**
  - Automation container per app with enablement flag.
- **ResourceAutomationEvent**
  - Trigger configuration for row changes or scheduled execution.
- **ResourceAutomationProcess**
  - Named process graph/unit scoped to a bot.
- **ResourceAutomationTask**
  - Executable task with typed task kind and config payload.

## Enums and Type Aliases

- **ResourceAutomationTriggerType**: `ROW_CREATED`, `ROW_UPDATED`, `ROW_DELETED`, `SCHEDULED`
- **ResourceAutomationTaskType**: `SEND_EMAIL`, `CALL_WEBHOOK`, `SET_COLUMN_VALUE`, `CREATE_ROW`
- **ResourceAutomationTaskScalar**: `str | int | float | bool | None`
- **ResourceAutomationTaskValue**: scalar, scalar-list, or scalar dictionary

## Aliases

- `Bot`, `Event`, `Process`, `Task`
- `TriggerType`, `TaskType`, `TaskScalar`, `TaskValue`

## Invariants

- Bot and process names must be non-empty after trimming.
- Scheduled events must not reference `table_id`.
- Row events (`ROW_CREATED/UPDATED/DELETED`) must include `table_id`.

## PlantUML

```plantuml
@startuml
hide empty members

enum ResourceAutomationTriggerType {
  ROW_CREATED
  ROW_UPDATED
  ROW_DELETED
  SCHEDULED
}

enum ResourceAutomationTaskType {
  SEND_EMAIL
  CALL_WEBHOOK
  SET_COLUMN_VALUE
  CREATE_ROW
}

class ResourceAutomationBot {
  +id: BotId
  +app_id: AppId
  +name: str
  +enabled: bool
}

class ResourceAutomationEvent {
  +id: EventId
  +bot_id: BotId
  +table_id: TableId?
  +trigger_type: ResourceAutomationTriggerType
  +condition_expression: str?
}

class ResourceAutomationProcess {
  +id: ProcessId
  +bot_id: BotId
  +name: str
}

class ResourceAutomationTask {
  +id: TaskId
  +process_id: ProcessId
  +type: ResourceAutomationTaskType
  +config_json: Map<String, ResourceAutomationTaskValue>
}

ResourceAutomationEvent --> ResourceAutomationBot : bot_id
ResourceAutomationProcess --> ResourceAutomationBot : bot_id
ResourceAutomationTask --> ResourceAutomationProcess : process_id
ResourceAutomationEvent --> ResourceAutomationTriggerType : trigger_type
ResourceAutomationTask --> ResourceAutomationTaskType : type

@enduml
```
