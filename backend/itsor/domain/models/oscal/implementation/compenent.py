from __future__ import annotations

from dataclasses import field
from typing import Literal
from uuid import UUID

from pydantic import Field

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids.oscal import OscalComponentDefinitionId
from itsor.domain.models.oscal.base import OscalBaseModel
from itsor.domain.models.oscal.common import ResponsibleRole
from itsor.domain.models.oscal.control.catalog import (
	BackMatter,
	Link,
	Metadata,
	Property,
)


class ImportComponentDefinition(OscalBaseModel):
	href: str
	remarks: str | None = None


class PortRange(OscalBaseModel):
	start: int | None = None
	end: int | None = None
	transport: Literal["TCP", "UDP"] | None = None
	remarks: str | None = None


class Protocol(OscalBaseModel):
	uuid: UUID | None = None
	name: str | None = None
	title: str | None = None
	port_ranges: list[PortRange] | None = Field(default=None, alias="port-ranges")


class SetParameter(OscalBaseModel):
	param_id: str = Field(alias="param-id")
	values: list[str] = Field(min_length=1)
	remarks: str | None = None


class Statement(OscalBaseModel):
	statement_id: str = Field(alias="statement-id")
	uuid: UUID
	description: str
	props: list[Property] | None = None
	links: list[Link] | None = None
	responsible_roles: list[ResponsibleRole] | None = Field(default=None, alias="responsible-roles")
	remarks: str | None = None


class ImplementedRequirement(OscalBaseModel):
	uuid: UUID
	control_id: str = Field(alias="control-id")
	description: str
	props: list[Property] | None = None
	links: list[Link] | None = None
	set_parameters: list[SetParameter] | None = Field(default=None, alias="set-parameters")
	responsible_roles: list[ResponsibleRole] | None = Field(default=None, alias="responsible-roles")
	statements: list[Statement] | None = None
	remarks: str | None = None


class ControlImplementation(OscalBaseModel):
	uuid: UUID
	source: str
	description: str
	implemented_requirements: list[ImplementedRequirement] = Field(
		alias="implemented-requirements",
		min_length=1,
	)
	props: list[Property] | None = None
	links: list[Link] | None = None
	set_parameters: list[SetParameter] | None = Field(default=None, alias="set-parameters")


class DefinedComponent(OscalBaseModel):
	uuid: UUID
	type: (
		Literal[
			"interconnection",
			"software",
			"hardware",
			"service",
			"policy",
			"physical",
			"process-procedure",
			"plan",
			"guidance",
			"standard",
			"validation",
		]
		| str
	)
	title: str
	description: str
	purpose: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	responsible_roles: list[ResponsibleRole] | None = Field(default=None, alias="responsible-roles")
	protocols: list[Protocol] | None = None
	control_implementations: list[ControlImplementation] | None = Field(
		default=None,
		alias="control-implementations",
	)
	remarks: str | None = None


class IncorporatesComponent(OscalBaseModel):
	component_uuid: UUID = Field(alias="component-uuid")
	description: str


class Capability(OscalBaseModel):
	uuid: UUID
	name: str
	description: str
	props: list[Property] | None = None
	links: list[Link] | None = None
	incorporates_components: list[IncorporatesComponent] | None = Field(
		default=None,
		alias="incorporates-components",
	)
	control_implementations: list[ControlImplementation] | None = Field(
		default=None,
		alias="control-implementations",
	)
	remarks: str | None = None


class ComponentDefinition(OscalBaseModel):
	id: OscalComponentDefinitionId = field(default_factory=typed_ulid_factory(OscalComponentDefinitionId), init=False)
	uuid: UUID
	metadata: Metadata
	import_component_definitions: list[ImportComponentDefinition] | None = Field(
		default=None,
		alias="import-component-definitions",
	)
	components: list[DefinedComponent] | None = None
	capabilities: list[Capability] | None = None
	back_matter: BackMatter | None = Field(default=None, alias="back-matter")


class OscalComponentDefinitionDocument(OscalBaseModel):
	schema_directive: str | None = Field(default=None, alias="$schema")
	component_definition: ComponentDefinition = Field(alias="component-definition")


class ImplementationStatus(OscalBaseModel):
	state: Literal["implemented", "partial", "planned", "alternative", "not-applicable"] | str
	remarks: str | None = None


class ComponentStatus(OscalBaseModel):
	state: Literal["under-development", "operational", "disposition", "other"]
	remarks: str | None = None


class SystemComponent(OscalBaseModel):
	uuid: UUID
	type: (
		Literal[
			"this-system",
			"system",
			"interconnection",
			"software",
			"hardware",
			"service",
			"policy",
			"physical",
			"process-procedure",
			"plan",
			"guidance",
			"standard",
			"validation",
			"network",
		]
		| str
	)
	title: str
	description: str
	status: ComponentStatus
	purpose: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	responsible_roles: list[ResponsibleRole] | None = Field(default=None, alias="responsible-roles")
	protocols: list[Protocol] | None = None
	remarks: str | None = None


class AuthorizedPrivilege(OscalBaseModel):
	title: str
	functions_performed: list[str] = Field(alias="functions-performed", min_length=1)
	description: str | None = None


class SystemUser(OscalBaseModel):
	uuid: UUID
	title: str | None = None
	short_name: str | None = Field(default=None, alias="short-name")
	description: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	role_ids: list[str] | None = Field(default=None, alias="role-ids")
	authorized_privileges: list[AuthorizedPrivilege] | None = Field(
		default=None,
		alias="authorized-privileges",
	)
	remarks: str | None = None


class ImplementedInventoryComponent(OscalBaseModel):
	component_uuid: UUID = Field(alias="component-uuid")
	props: list[Property] | None = None
	links: list[Link] | None = None
	responsible_parties: list[ResponsibleRole] | None = Field(
		default=None,
		alias="responsible-parties",
	)
	remarks: str | None = None


class InventoryItem(OscalBaseModel):
	uuid: UUID
	description: str
	props: list[Property] | None = None
	links: list[Link] | None = None
	responsible_parties: list[ResponsibleRole] | None = Field(
		default=None,
		alias="responsible-parties",
	)
	implemented_components: list[ImplementedInventoryComponent] | None = Field(
		default=None,
		alias="implemented-components",
	)
	remarks: str | None = None


class SystemId(OscalBaseModel):
	id: str
	identifier_type: str | None = Field(default=None, alias="identifier-type")


__all__ = [
	"Capability",
	"ComponentDefinition",
	"ControlImplementation",
	"DefinedComponent",
	"ImplementedRequirement",
	"ImportComponentDefinition",
	"IncorporatesComponent",
	"OscalComponentDefinitionDocument",
	"Protocol",
	"SetParameter",
	"Statement",
	"SystemComponent",
	"SystemId",
	"SystemUser",
]
