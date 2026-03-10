# Resource Schema Models

Source: `backend/itsor/domain/models/resource_models/schema_models.py`

---

## Purpose

Defines schema metadata for table-driven resources: tables, attributes (columns), slices, and security rules.

## Models

- **Table**
  - App-scoped table metadata with optional primary key and label column.
- **ResourceAttribute**
  - Column metadata with type, requirement flags, formulas, and optional table reference.
- **ResourceSlice**
  - Named slice over a table with optional row filter and explicit column list.
- **ResourceSecurityRule**
  - Table-level filter expression for security constraints.

## Enums and Aliases

- **ResourceAttributeType**: `TEXT`, `NUMBER`, `BOOLEAN`, `DATE`, `ENUM`, `REF`, `FILE`, `IMAGE`, `LOCATION`
- Aliases:
  - `Column = ResourceAttribute`
  - `ColumnType = ResourceAttributeType`
  - `Slice = ResourceSlice`
  - `SecurityRule = ResourceSecurityRule`

## Invariants

- `Table.name`, `ResourceAttribute.name`, and `ResourceSlice.name` must be non-empty after trim.
- `ResourceAttribute` rules:
  - `REF` columns require `ref_table_id`.
  - non-`REF` columns must not set `ref_table_id`.
  - virtual columns require a `formula`.
- `ResourceSecurityRule.filter_expression` must be non-empty after trim.

## PlantUML

```plantuml
@startuml
hide empty members

enum ResourceAttributeType {
  TEXT
  NUMBER
  BOOLEAN
  DATE
  ENUM
  REF
  FILE
  IMAGE
  LOCATION
}

class Table {
  +id: TableId
  +app_id: AppId
  +name: str
  +data_source_id: str?
  +primary_key: ColumnId?
  +label_column: ColumnId?
}

class ResourceAttribute {
  +id: ColumnId
  +table_id: TableId
  +name: str
  +type: ResourceAttributeType
  +is_key: bool
  +is_label: bool
  +is_required: bool
  +is_virtual: bool
  +formula: str?
  +ref_table_id: TableId?
}

class ResourceSlice {
  +id: SliceId
  +app_id: AppId
  +name: str
  +table_id: TableId
  +row_filter_expression: str?
  +column_list: List<ColumnId>
}

class ResourceSecurityRule {
  +id: SecurityRuleId
  +table_id: TableId
  +filter_expression: str
}

ResourceAttribute --> Table : table_id
ResourceAttribute --> ResourceAttributeType : type
ResourceAttribute --> Table : ref_table_id (for REF)
ResourceSlice --> Table : table_id
ResourceSlice --> ColumnId : column_list
ResourceSecurityRule --> Table : table_id

@enduml
```
