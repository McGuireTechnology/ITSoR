from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from itsor.domain._ulid import typed_ulid_factory


def _normalize_required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} is required")
    return normalized


class ItamCisControlFamily(str, Enum):
    ENTERPRISE_ASSET_INVENTORY = "1"
    SOFTWARE_ASSET_INVENTORY = "2"
    DATA_INVENTORY = "3"
    ACCOUNT_INVENTORY = "5"
    SERVICE_PROVIDER_INVENTORY = "15"


class ItamFindingSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class FrameworkDefinition:
    id: str
    name: str
    version: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", _normalize_required_text(self.id, "framework id"))
        object.__setattr__(self, "name", _normalize_required_text(self.name, "framework name"))
        if self.version is not None:
            object.__setattr__(
                self,
                "version",
                _normalize_required_text(self.version, "framework version"),
            )


CIS_CONTROLS_V81 = FrameworkDefinition(
    id="CIS-Controls-v8.1", name="CIS Critical Security Controls", version="8.1"
)
NIST_CSF_20 = FrameworkDefinition(
    id="NIST-CSF-2.0", name="NIST Cybersecurity Framework", version="2.0"
)
HIPAA_SECURITY_RULE = FrameworkDefinition(
    id="HIPAA-Security-Rule", name="HIPAA Security Rule"
)

KNOWN_FRAMEWORKS: tuple[FrameworkDefinition, ...] = (
    CIS_CONTROLS_V81,
    NIST_CSF_20,
    HIPAA_SECURITY_RULE,
)


@dataclass(frozen=True)
class ItamSafeguardDefinition:
    safeguard_id: str
    title: str
    description: str
    family: ItamCisControlFamily

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "safeguard_id",
            _normalize_required_text(self.safeguard_id, "safeguard_id"),
        )
        object.__setattr__(self, "title", _normalize_required_text(self.title, "title"))
        object.__setattr__(
            self,
            "description",
            _normalize_required_text(self.description, "description"),
        )


@dataclass(frozen=True)
class ItamEvidenceRecord:
    collected_at: datetime
    source: str
    artifact_ref: str
    notes: str = ""

    def __post_init__(self) -> None:
        if self.collected_at.tzinfo is None:
            raise ValueError("collected_at must be timezone-aware")
        object.__setattr__(self, "source", _normalize_required_text(self.source, "source"))
        object.__setattr__(
            self,
            "artifact_ref",
            _normalize_required_text(self.artifact_ref, "artifact_ref"),
        )
        object.__setattr__(self, "notes", self.notes.strip())


@dataclass(frozen=True)
class ItamControlFinding:
    safeguard_id: str
    summary: str
    severity: ItamFindingSeverity
    framework_id: str = CIS_CONTROLS_V81.id
    observed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "safeguard_id",
            _normalize_required_text(self.safeguard_id, "safeguard_id"),
        )
        object.__setattr__(self, "summary", _normalize_required_text(self.summary, "summary"))
        object.__setattr__(
            self,
            "framework_id",
            _normalize_required_text(self.framework_id, "framework_id"),
        )
        if self.observed_at.tzinfo is None:
            raise ValueError("observed_at must be timezone-aware")


class InventoryCategory(str, Enum):
    ENTERPRISE_ASSETS = "enterprise_assets"
    SOFTWARE_ASSETS = "software_assets"
    DATA_ASSETS = "data_assets"
    ACCOUNTS = "accounts"
    SERVICE_PROVIDERS = "service_providers"


@dataclass(frozen=True)
class InventoryFieldDefinition:
    term: str
    sheet: str
    cis_ig1_required: bool
    description: str
    example: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "term", _normalize_required_text(self.term, "term"))
        object.__setattr__(self, "sheet", _normalize_required_text(self.sheet, "sheet"))
        object.__setattr__(
            self,
            "description",
            _normalize_required_text(self.description, "description"),
        )
        object.__setattr__(self, "example", self.example.strip())


@dataclass(frozen=True)
class InventorySchema:
    schema_id: str
    framework_id: str
    category: InventoryCategory
    safeguard_id: str
    name: str
    fields: tuple[InventoryFieldDefinition, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "schema_id",
            _normalize_required_text(self.schema_id, "schema_id"),
        )
        object.__setattr__(
            self,
            "framework_id",
            _normalize_required_text(self.framework_id, "framework_id"),
        )
        object.__setattr__(
            self,
            "safeguard_id",
            _normalize_required_text(self.safeguard_id, "safeguard_id"),
        )
        object.__setattr__(self, "name", _normalize_required_text(self.name, "name"))
        if not self.fields:
            raise ValueError("fields is required")

    @property
    def required_terms(self) -> tuple[str, ...]:
        return tuple(field.term for field in self.fields if field.cis_ig1_required)


@dataclass(frozen=True)
class AssetClassDefinition:
    name: str
    domain: str
    parent_name: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _normalize_required_text(self.name, "name"))
        object.__setattr__(self, "domain", _normalize_required_text(self.domain, "domain"))
        if self.parent_name is not None:
            object.__setattr__(
                self,
                "parent_name",
                _normalize_required_text(self.parent_name, "parent_name"),
            )


InventoryRecordId = str


@dataclass
class InventoryRecord:
    id: InventoryRecordId = field(default_factory=typed_ulid_factory(str), init=False)
    schema_id: str = ""
    framework_id: str = ""
    values: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.schema_id = _normalize_required_text(self.schema_id, "schema_id")
        self.framework_id = _normalize_required_text(self.framework_id, "framework_id")
        normalized_values: dict[str, Any] = {}
        for key, value in self.values.items():
            normalized_key = _normalize_required_text(str(key), "values key")
            normalized_values[normalized_key] = value
        self.values = normalized_values

    def validate_required_fields(self, schema: InventorySchema) -> None:
        if schema.schema_id != self.schema_id:
            raise ValueError("schema_id does not match provided schema")
        if schema.framework_id != self.framework_id:
            raise ValueError("framework_id does not match provided schema")

        missing = [
            term
            for term in schema.required_terms
            if term not in self.values or self.values[term] in (None, "")
        ]
        if missing:
            raise ValueError(f"missing required inventory fields: {', '.join(sorted(missing))}")


CIS_ITAM_BASELINE: tuple[ItamSafeguardDefinition, ...] = (
    ItamSafeguardDefinition(
        safeguard_id="1.1",
        title="Establish and Maintain Detailed Enterprise Asset Inventory",
        description="Maintain an enterprise asset inventory with ownership, location, and lifecycle details.",
        family=ItamCisControlFamily.ENTERPRISE_ASSET_INVENTORY,
    ),
    ItamSafeguardDefinition(
        safeguard_id="2.1",
        title="Establish and Maintain a Software Inventory",
        description="Maintain an authorized software inventory across enterprise assets.",
        family=ItamCisControlFamily.SOFTWARE_ASSET_INVENTORY,
    ),
    ItamSafeguardDefinition(
        safeguard_id="3.2",
        title="Establish and Maintain a Data Inventory",
        description="Maintain inventory and ownership for sensitive and business-critical data.",
        family=ItamCisControlFamily.DATA_INVENTORY,
    ),
    ItamSafeguardDefinition(
        safeguard_id="5.1",
        title="Establish and Maintain an Inventory of Accounts",
        description="Maintain account inventory and ownership details for accountability.",
        family=ItamCisControlFamily.ACCOUNT_INVENTORY,
    ),
    ItamSafeguardDefinition(
        safeguard_id="15.1",
        title="Establish and Maintain an Inventory of Service Providers",
        description="Maintain external service provider inventory, ownership, and contracts.",
        family=ItamCisControlFamily.SERVICE_PROVIDER_INVENTORY,
    ),
)


def default_cis_itam_safeguards() -> dict[str, ItamSafeguardDefinition]:
    return {safeguard.safeguard_id: safeguard for safeguard in CIS_ITAM_BASELINE}


def _field(
    term: str,
    sheet: str,
    cis_ig1_minimum: str,
    description: str,
    example: str,
) -> InventoryFieldDefinition:
    return InventoryFieldDefinition(
        term=term,
        sheet=sheet,
        cis_ig1_required=cis_ig1_minimum.strip().lower() == "yes",
        description=description,
        example=example,
    )


_ENTERPRISE_FIELDS: tuple[InventoryFieldDefinition, ...] = (
    _field("Enterprise Asset Identifier", "Enterprise Asset Inventory v8.1", "Yes", "A unique ID that can be used to identify an asset.", "458369"),
    _field("Asset Sub-Class", "Enterprise Asset Inventory v8.1", "", "A CIS Controls asset subclass that can be customized by the enterprise.", "End-User Device"),
    _field("Date of Purchase", "Enterprise Asset Inventory v8.1", "Yes", "The purchase date of the asset.", "1/1/2025"),
    _field("Purchase Price", "Enterprise Asset Inventory v8.1", "Yes", "The purchase price of the asset.", "$1,020.00"),
    _field("Item Description", "Enterprise Asset Inventory v8.1", "Yes", "A general description of the enterprise asset.", "ABC Laptop XPS 16"),
    _field("Manufacturer", "Enterprise Asset Inventory v8.1", "Yes", "The manufacturer of the asset.", "ABC"),
    _field("Model Number", "Enterprise Asset Inventory v8.1", "Yes", "The model number identifying the product line.", "9640"),
    _field("Serial Number", "Enterprise Asset Inventory v8.1", "Yes", "Manufacturer serial number identifying the asset.", "CN-0546871-1536-165465-0564Q"),
    _field("Name of the Enterprise Asset Owner", "Enterprise Asset Inventory v8.1", "Yes", "Workforce member responsible for the asset.", "John Smith"),
    _field("Machine Name", "Enterprise Asset Inventory v8.1", "Yes", "Assigned machine name used for identification and management.", "JSMITH-09"),
    _field("Business Unit", "Enterprise Asset Inventory v8.1", "Yes", "Business unit where the asset owner resides.", "Sales"),
    _field("Physical Location of Enterprise Asset", "Enterprise Asset Inventory v8.1", "Yes", "Physical location of the enterprise asset.", "Headquarters Cubicle 4G"),
    _field("Physical (MAC) Address", "Enterprise Asset Inventory v8.1", "Yes", "NIC MAC address for the enterprise asset.", "00:1A:2B:3C:4D:5E"),
    _field("IP Address", "Enterprise Asset Inventory v8.1", "Yes", "Internal or external network address associated with the asset.", "192.168.123.132"),
    _field("Warranty Expiration Date", "Enterprise Asset Inventory v8.1", "Yes", "Asset warranty expiration date.", "1/1/2027"),
    _field("Any Relevant Licensing Information", "Enterprise Asset Inventory v8.1", "Yes", "Licensing details relevant to the asset.", "Product support included in license"),
    _field("Approval to Connect to Enterprise Network?", "Enterprise Asset Inventory v8.1", "Yes", "Whether the asset is approved to connect to the network.", "Yes"),
    _field("IT Verification of Enterprise Asset Inventory", "Enterprise Asset Inventory v8.1", "Yes", "Last verification date by IT.", "6/1/2025"),
    _field("Disposal Date", "Enterprise Asset Inventory v8.1", "", "Date the asset was disposed of.", "1/1/2027"),
    _field("Disposal Type (Controlled/Uncontrolled)", "Enterprise Asset Inventory v8.1", "", "Method or type of disposal.", "Hard drive shredded through data destruction service on-site."),
)

_SOFTWARE_FIELDS: tuple[InventoryFieldDefinition, ...] = (
    _field("Software Title", "Software Asset Inventory v8.1", "Yes", "Title or name of the software.", "Software ABC"),
    _field("Business Purpose", "Software Asset Inventory v8.1", "Yes", "Business justification for the software.", "Used as the enterprise's enterprise resource planning tool"),
    _field("Asset Sub-Class", "Software Asset Inventory v8.1", "", "CIS Controls software subclass that can be customized.", "Application"),
    _field("Developer/Publisher of Software", "Software Asset Inventory v8.1", "Yes", "Developer or publisher of the software.", "XYZ Corp."),
    _field("Acquisition Date", "Software Asset Inventory v8.1", "Yes", "Date the software was acquired.", "1/1/2025"),
    _field("Initial Install/Use Date", "Software Asset Inventory v8.1", "Yes", "Date the software was first installed or used.", "3/1/2025"),
    _field("Duration of Usage", "Software Asset Inventory v8.1", "Yes", "Duration of software usage since installation.", "2 months"),
    _field("URL", "Software Asset Inventory v8.1", "Yes", "URL for more software information.", "https://xyc.com/abc"),
    _field("App Store(s)", "Software Asset Inventory v8.1", "Yes", "Referenced app store if applicable.", "N/A"),
    _field("Version(s)", "Software Asset Inventory v8.1", "Yes", "Version or versions of software.", "1.1.1"),
    _field("Deployment Mechanism", "Software Asset Inventory v8.1", "Yes", "Software deployment method.", "Basic Deployment"),
    _field("End-of-life (EoL)/End-of-support (EoS) Date", "Software Asset Inventory v8.1", "Yes", "Date software is no longer supported and should be retired.", "1/1/2028"),
    _field("Decommission Date", "Software Asset Inventory v8.1", "Yes", "Date software is no longer in use.", "1/1/2028"),
    _field("Any Relevant Licensing Information", "Software Asset Inventory v8.1", "Yes", "Licensing details relevant to the software.", "Subscription/Term licensing"),
    _field("Number of Licenses", "Software Asset Inventory v8.1", "", "Number of software licenses procured.", "4"),
)

_DATA_FIELDS: tuple[InventoryFieldDefinition, ...] = (
    _field("Data Name", "Data Inventory v8.1", "Yes", "Short name or identifier for data.", "eCommerce Platform"),
    _field("Asset Sub-Class", "Data Inventory v8.1", "", "CIS Controls data subclass that can be customized.", "Database"),
    _field("Data Type (Financial, Customer, etc.)", "Data Inventory v8.1", "", "Type of data being inventoried.", "Financial, operational"),
    _field("Description", "Data Inventory v8.1", "", "Brief description of the data.", "A platform for eCommerce transactions"),
    _field("Data Location", "Data Inventory v8.1", "", "Physical or digital location of the data.", "Cloud Company A"),
    _field("Data Format", "Data Inventory v8.1", "", "Format used to arrange/store/transmit data.", "Relational Database"),
    _field("Data Owner", "Data Inventory v8.1", "Yes", "Person responsible for the data.", "John Smith"),
    _field("Data Classification", "Data Inventory v8.1", "", "Sensitivity and regulatory classification of data.", "Sensitive"),
    _field("Business Purpose", "Data Inventory v8.1", "", "Business justification for the data use.", "To store eCommerce transactions"),
    _field("Data Retention Limits", "Data Inventory v8.1", "Yes", "Length of time data is retained.", "3 years"),
    _field("Disposal Method", "Data Inventory v8.1", "Yes", "Method used to dispose of the data.", "Records deleted permanently (purged) after 3 years"),
    _field("Disposal Date", "Data Inventory v8.1", "Yes", "Date data was disposed.", "1/1/2025"),
)

_ACCOUNT_FIELDS: tuple[InventoryFieldDefinition, ...] = (
    _field("Associated Service Provider or Product", "Account Inventory v8.1", "Yes", "Service provider or product associated with the account.", "Active Directory"),
    _field("Account Owner", "Account Inventory v8.1", "Yes", "Workforce member assigned and responsible for the account.", "John Smith"),
    _field("Account Type", "Account Inventory v8.1", "", "CIS Controls account classification.", "User Account"),
    _field("Username", "Account Inventory v8.1", "Yes", "Unique identifier used to sign in.", "jsmith-09"),
    _field("Account Creation Date", "Account Inventory v8.1", "Yes", "Date account was created.", "1/1/2025"),
    _field("Account Deletion Date", "Account Inventory v8.1", "Yes", "Date account was deleted.", "N/A"),
    _field("Account Expiration Date", "Account Inventory v8.1", "Yes", "Date account expires.", "N/A"),
    _field("Account Status (Enabled, Disabled, Deleted, Dormant, Locked)", "Account Inventory v8.1", "Yes", "Current account status.", "Enabled"),
    _field("MFA Enabled?", "Account Inventory v8.1", "Yes", "Whether MFA is enabled for the account.", "Yes"),
    _field("Review Date (Date Validated)", "Account Inventory v8.1", "Yes", "Last date account was validated.", "3/1/2025"),
    _field("Business Unit", "Account Inventory v8.1", "Yes", "Business unit where the account owner resides.", "Sales"),
)

_SERVICE_PROVIDER_FIELDS: tuple[InventoryFieldDefinition, ...] = (
    _field("Service Provider Name", "Service Provider Inventory v8.1", "Yes", "Name of the service provider.", "Cloud Company A"),
    _field("Service Provider Classification", "Service Provider Inventory v8.1", "Yes", "Classification of the service provider.", "Standard"),
    _field("Service Provider Point of Contact", "Service Provider Inventory v8.1", "Yes", "Provider-side contact responsible for enterprise support.", "Joe Smith/jsmith@cloudcompanya.com"),
    _field("Enterprise Point of Contact", "Service Provider Inventory v8.1", "Yes", "Enterprise contact responsible for the provider.", "John Smith/jsmith@enterprisea.com"),
    _field("Business Unit", "Service Provider Inventory v8.1", "Yes", "Business unit that uses the service provider.", "Sales"),
    _field("Description", "Service Provider Inventory v8.1", "", "Short description of provider service.", "Provides platform for eCommerce database"),
    _field("Contract Start Date", "Service Provider Inventory v8.1", "", "Contract start date.", "1/1/2025"),
    _field("Contract Expire Date", "Service Provider Inventory v8.1", "", "Contract expiration date.", "1/1/2026"),
    _field("Contract Review Date", "Service Provider Inventory v8.1", "Yes", "Last date contract was reviewed.", "1/1/2026"),
)

CIS_INVENTORY_SCHEMAS: tuple[InventorySchema, ...] = (
    InventorySchema(
        schema_id="cis-1.1-enterprise-asset-inventory",
        framework_id=CIS_CONTROLS_V81.id,
        category=InventoryCategory.ENTERPRISE_ASSETS,
        safeguard_id="1.1",
        name="Enterprise Asset Inventory v8.1",
        fields=_ENTERPRISE_FIELDS,
    ),
    InventorySchema(
        schema_id="cis-2.1-software-asset-inventory",
        framework_id=CIS_CONTROLS_V81.id,
        category=InventoryCategory.SOFTWARE_ASSETS,
        safeguard_id="2.1",
        name="Software Asset Inventory v8.1",
        fields=_SOFTWARE_FIELDS,
    ),
    InventorySchema(
        schema_id="cis-3.2-data-inventory",
        framework_id=CIS_CONTROLS_V81.id,
        category=InventoryCategory.DATA_ASSETS,
        safeguard_id="3.2",
        name="Data Inventory v8.1",
        fields=_DATA_FIELDS,
    ),
    InventorySchema(
        schema_id="cis-5.1-account-inventory",
        framework_id=CIS_CONTROLS_V81.id,
        category=InventoryCategory.ACCOUNTS,
        safeguard_id="5.1",
        name="Account Inventory v8.1",
        fields=_ACCOUNT_FIELDS,
    ),
    InventorySchema(
        schema_id="cis-15.1-service-provider-inventory",
        framework_id=CIS_CONTROLS_V81.id,
        category=InventoryCategory.SERVICE_PROVIDERS,
        safeguard_id="15.1",
        name="Service Provider Inventory v8.1",
        fields=_SERVICE_PROVIDER_FIELDS,
    ),
)

CIS_ASSET_CLASSES_V81: tuple[AssetClassDefinition, ...] = (
    AssetClassDefinition(name="Enterprise Assets", domain="Devices"),
    AssetClassDefinition(name="End-user Devices", domain="Devices", parent_name="Enterprise Assets"),
    AssetClassDefinition(name="Portable", domain="Devices", parent_name="End-user Devices"),
    AssetClassDefinition(name="Mobile", domain="Devices", parent_name="Portable"),
    AssetClassDefinition(name="Servers", domain="Devices", parent_name="Enterprise Assets"),
    AssetClassDefinition(name="Internet of Things (IoT) and Non-computing Devices", domain="Devices", parent_name="Enterprise Assets"),
    AssetClassDefinition(name="Network Devices", domain="Devices", parent_name="Enterprise Assets"),
    AssetClassDefinition(name="Removable Media", domain="Devices"),
    AssetClassDefinition(name="Applications", domain="Software"),
    AssetClassDefinition(name="Services", domain="Software", parent_name="Applications"),
    AssetClassDefinition(name="Libraries", domain="Software", parent_name="Applications"),
    AssetClassDefinition(name="APIs", domain="Software", parent_name="Applications"),
    AssetClassDefinition(name="Operating Systems", domain="Software"),
    AssetClassDefinition(name="Services", domain="Software", parent_name="Operating Systems"),
    AssetClassDefinition(name="Libraries", domain="Software", parent_name="Operating Systems"),
    AssetClassDefinition(name="APIs", domain="Software", parent_name="Operating Systems"),
    AssetClassDefinition(name="Firmware", domain="Software"),
    AssetClassDefinition(name="Sensitive Data", domain="Data"),
    AssetClassDefinition(name="Log Data", domain="Data"),
    AssetClassDefinition(name="Physical Data", domain="Data"),
    AssetClassDefinition(name="Workforce", domain="Users"),
    AssetClassDefinition(name="Service Providers", domain="Users"),
    AssetClassDefinition(name="User Accounts", domain="Users"),
    AssetClassDefinition(name="Administrator Accounts", domain="Users"),
    AssetClassDefinition(name="Service Accounts", domain="Users"),
    AssetClassDefinition(name="Network Infrastructure", domain="Network"),
    AssetClassDefinition(name="Network Architecture", domain="Network"),
    AssetClassDefinition(name="Plans", domain="Documentation"),
    AssetClassDefinition(name="Policies", domain="Documentation"),
    AssetClassDefinition(name="Processes", domain="Documentation"),
    AssetClassDefinition(name="Procedures", domain="Documentation"),
)


__all__ = [
    "AssetClassDefinition",
    "CIS_ASSET_CLASSES_V81",
    "CIS_CONTROLS_V81",
    "CIS_INVENTORY_SCHEMAS",
    "CIS_ITAM_BASELINE",
    "FrameworkDefinition",
    "HIPAA_SECURITY_RULE",
    "InventoryCategory",
    "InventoryFieldDefinition",
    "InventoryRecord",
    "InventorySchema",
    "ItamCisControlFamily",
    "ItamControlFinding",
    "ItamEvidenceRecord",
    "ItamFindingSeverity",
    "ItamSafeguardDefinition",
    "KNOWN_FRAMEWORKS",
    "NIST_CSF_20",
    "default_cis_itam_safeguards",
]
