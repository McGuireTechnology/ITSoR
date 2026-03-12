from itsor.domain.models.itam import (
    CIS_ASSET_CLASSES_V81,
    CIS_CONTROLS_V81,
    CIS_INVENTORY_SCHEMAS,
    HIPAA_SECURITY_RULE,
    InventoryCategory,
    InventoryFieldDefinition,
    InventoryRecord,
    InventorySchema,
    default_cis_itam_safeguards,
)


def test_cis_inventory_safeguards_cover_expected_ids() -> None:
    safeguards = default_cis_itam_safeguards()

    assert set(safeguards) == {"1.1", "2.1", "3.2", "5.1", "15.1"}


def test_cis_inventory_schemas_cover_expected_categories() -> None:
    schema_ids = {schema.safeguard_id for schema in CIS_INVENTORY_SCHEMAS}
    categories = {schema.category for schema in CIS_INVENTORY_SCHEMAS}

    assert schema_ids == {"1.1", "2.1", "3.2", "5.1", "15.1"}
    assert categories == {
        InventoryCategory.ENTERPRISE_ASSETS,
        InventoryCategory.SOFTWARE_ASSETS,
        InventoryCategory.DATA_ASSETS,
        InventoryCategory.ACCOUNTS,
        InventoryCategory.SERVICE_PROVIDERS,
    }
    assert all(schema.framework_id == CIS_CONTROLS_V81.id for schema in CIS_INVENTORY_SCHEMAS)


def test_inventory_record_validates_cis_required_fields() -> None:
    schema = next(
        item for item in CIS_INVENTORY_SCHEMAS if item.category == InventoryCategory.ENTERPRISE_ASSETS
    )

    valid_payload = {
        "Enterprise Asset Identifier": "asset-001",
        "Date of Purchase": "2025-01-01",
        "Purchase Price": "$1200",
        "Item Description": "Laptop",
        "Manufacturer": "ABC",
        "Model Number": "XPS16",
        "Serial Number": "SN-001",
        "Name of the Enterprise Asset Owner": "Jane Smith",
        "Machine Name": "JSMITH-01",
        "Business Unit": "Sales",
        "Physical Location of Enterprise Asset": "HQ",
        "Physical (MAC) Address": "00:1A:2B:3C:4D:5E",
        "IP Address": "192.168.1.10",
        "Warranty Expiration Date": "2027-01-01",
        "Any Relevant Licensing Information": "Support included",
        "Approval to Connect to Enterprise Network?": "Yes",
        "IT Verification of Enterprise Asset Inventory": "2025-06-01",
    }

    record = InventoryRecord(
        schema_id=schema.schema_id,
        framework_id=schema.framework_id,
        values=valid_payload,
    )
    record.validate_required_fields(schema)


def test_inventory_record_rejects_missing_required_fields() -> None:
    schema = next(
        item for item in CIS_INVENTORY_SCHEMAS if item.category == InventoryCategory.ACCOUNTS
    )
    record = InventoryRecord(
        schema_id=schema.schema_id,
        framework_id=schema.framework_id,
        values={"Account Owner": "Jane Smith"},
    )

    try:
        record.validate_required_fields(schema)
    except ValueError as exc:
        message = str(exc)
    else:
        raise AssertionError("Expected missing required inventory fields error")

    assert "missing required inventory fields" in message
    assert "Username" in message


def test_additional_framework_schema_supported() -> None:
    schema = InventorySchema(
        schema_id="hipaa-164-308-a1-workforce-security",
        framework_id=HIPAA_SECURITY_RULE.id,
        category=InventoryCategory.ACCOUNTS,
        safeguard_id="164.308(a)(3)(i)",
        name="HIPAA Workforce Security Inventory",
        fields=(
            InventoryFieldDefinition(
                term="Workforce Member",
                sheet="HIPAA Security Rule",
                cis_ig1_required=True,
                description="Assigned workforce member.",
                example="John Smith",
            ),
        ),
    )

    assert schema.framework_id == "HIPAA-Security-Rule"


def test_cis_asset_classes_include_expected_inventory_domains() -> None:
    domains = {entry.domain for entry in CIS_ASSET_CLASSES_V81}

    assert domains == {"Devices", "Software", "Data", "Users", "Network", "Documentation"}
