# CIS Inventory Domain Model Baseline

This baseline introduces framework-aware inventory domain models for ITAM so ITSoR can start with CIS Controls v8.1 and extend to additional frameworks such as NIST CSF 2.0 and HIPAA Security Rule.

## Scope

The current CIS baseline covers inventory schemas aligned to these safeguards:

- `1.1` Enterprise Asset Inventory
- `2.1` Software Asset Inventory
- `3.2` Data Inventory
- `5.1` Account Inventory
- `15.1` Service Provider Inventory

## Domain model additions

In `backend/itsor/domain/models/itam/control_models.py`, the domain now defines:

- `FrameworkDefinition` with built-in constants for:
  - `CIS-Controls-v8.1`
  - `NIST-CSF-2.0`
  - `HIPAA-Security-Rule`
- `InventorySchema` and `InventoryFieldDefinition` for schema-level inventory definitions.
- `InventoryRecord` for submitted inventory entries with required-field validation.
- `AssetClassDefinition` and `CIS_ASSET_CLASSES_V81` for CIS v8.1 asset class taxonomy coverage.

## CIS legend alignment

`CIS_INVENTORY_SCHEMAS` is seeded from the supplied CIS legend terms for all five inventory tabs.

Each schema includes:

- Full field list (term, description, example)
- CIS IG1 required flag (`cis_ig1_required`)
- Safeguard ID and inventory category linkage

## Extending to other frameworks

To support additional frameworks now:

1. Define a `FrameworkDefinition` constant.
2. Add one or more `InventorySchema` definitions tied to that framework ID.
3. Reuse `InventoryRecord.validate_required_fields` for framework-specific required field enforcement.

This keeps domain logic stable while allowing new compliance overlays without changing the core inventory entity model.
