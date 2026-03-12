from __future__ import annotations

from dataclasses import field
from uuid import UUID

from pydantic import Field

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids.oscal import OscalSystemSecurityPlanId
from itsor.domain.models.oscal.base import OscalBaseModel
from itsor.domain.models.oscal.control.catalog import BackMatter, Link, Metadata, Property
from itsor.domain.models.oscal.implementation.compenent import SystemId


class SystemCharacteristics(OscalBaseModel):
	system_name: str = Field(alias="system-name")
	description: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None


class SystemImplementation(OscalBaseModel):
	uuid: UUID
	description: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None


class SystemSecurityPlan(OscalBaseModel):
	id: OscalSystemSecurityPlanId = field(default_factory=typed_ulid_factory(OscalSystemSecurityPlanId), init=False)
	uuid: UUID
	metadata: Metadata
	system_characteristics: SystemCharacteristics = Field(alias="system-characteristics")
	system_implementation: SystemImplementation | None = Field(default=None, alias="system-implementation")
	system_id: SystemId | None = Field(default=None, alias="system-id")
	back_matter: BackMatter | None = Field(default=None, alias="back-matter")


class OscalSystemSecurityPlanDocument(OscalBaseModel):
	schema_directive: str | None = Field(default=None, alias="$schema")
	system_security_plan: SystemSecurityPlan = Field(alias="system-security-plan")


__all__ = [
	"OscalSystemSecurityPlanDocument",
	"SystemCharacteristics",
	"SystemImplementation",
	"SystemSecurityPlan",
]
