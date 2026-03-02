# IT Asset Management Domain Models

ITAM models provide authoritative inventory, ownership, lifecycle, and financial/compliance context for technology assets.

## Scope

- Hardware, software, cloud, and SaaS asset inventories
- Ownership, custody, assignment, and location tracking
- Lifecycle, depreciation, warranty, contract, and license management
- Asset-to-control and asset-to-risk linkage for assurance and audit

## Core Entities

| Entity | Purpose | Required Fields |
| --- | --- | --- |
| `asset` | Canonical asset record | `asset_id`, `asset_type`, `display_name`, `state`, `criticality`, `owner_identity_id`, `source_system`, `valid_from`, `valid_to` |
| `hardware_asset` | Physical endpoint/device detail | `asset_id`, `serial_number`, `manufacturer`, `model`, `purchase_date`, `warranty_end` |
| `software_asset` | Installed or managed software product | `asset_id`, `product_name`, `version`, `publisher`, `deployment_scope` |
| `cloud_resource_asset` | Cloud-native resource detail | `asset_id`, `provider`, `account_id`, `region`, `resource_type`, `resource_native_id` |
| `license_entitlement` | License right pool and constraints | `license_id`, `sku`, `metric`, `quantity_owned`, `quantity_used`, `renewal_date`, `state` |
| `asset_assignment` | Person/team/workload assignment history | `assignment_id`, `asset_id`, `assignee_identity_id`, `assigned_at`, `returned_at`, `status` |
| `maintenance_contract` | Support and warranty agreements | `contract_id`, `vendor`, `start_at`, `end_at`, `sla_tier`, `state` |
| `cmdb_ci_link` | Link to service/configuration context | `link_id`, `asset_id`, `ci_id`, `relationship_type`, `valid_from`, `valid_to` |

## Key Relationships

- `asset` `is_specialized_as` `hardware_asset` / `software_asset` / `cloud_resource_asset`
- `asset` `is_assigned_to` `asset_assignment`
- `software_asset` `consumes` `license_entitlement`
- `asset` `is_covered_by` `maintenance_contract`
- `asset` `maps_to` service/configuration item via `cmdb_ci_link`
- `asset` `is_target_of` GRC control assertions and risk entries

## Lifecycle States

### `asset.state`

- `planned`
- `procured`
- `in_service`
- `quarantined`
- `retired`
- `disposed`

### `license_entitlement.state`

- `active`
- `expiring`
- `expired`
- `terminated`

## Financial and Compliance Views

- `asset_cost_view`: capex/opex, depreciation method, carrying value
- `license_position_view`: entitlement vs consumption variance
- `support_coverage_view`: warranty/contract coverage gaps
- `compliance_posture_view`: missing controls, unsupported software, unauthorized assets

## Standards Alignment

| Standard | Mapping |
| --- | --- |
| ITIL v4 | IT Asset Management, Service Configuration Management, Change Enablement |
| CIS Controls v8 | Control 1 (Inventory and Control of Enterprise Assets), Control 2 (Inventory and Control of Software Assets) |
| NIST CSF 2.0 | `ID.AM` (Asset Management), `PR.PS` (Platform Security), `DE.CM` monitoring support |
| ISO/IEC 19770 | IT asset and software asset management processes and data quality |
| ISO/IEC 27001:2022 | Asset inventory, ownership, acceptable use, and lifecycle security controls |

## Cross-Slice Dependencies

- Asset owners and custodians resolve to IDM identities.
- Tenant and group context resolve via Platform slice.
- Control assertions/evidence resolve via GRC slice.
