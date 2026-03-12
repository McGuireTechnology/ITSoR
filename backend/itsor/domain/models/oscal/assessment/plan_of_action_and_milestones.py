from __future__ import annotations

from dataclasses import field
from uuid import UUID

from pydantic import Field

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids.oscal import OscalPoamId, OscalPoamItemId
from itsor.domain.models.oscal.base import OscalBaseModel
from itsor.domain.models.oscal.assessment.plan import AssessmentAssets, ImportSsp
from itsor.domain.models.oscal.assessment.results import (
	Finding,
	Observation,
	Origin,
	RelatedObservation,
	AssociatedRisk,
	Risk,
)
from itsor.domain.models.oscal.control.catalog import (
	BackMatter,
	Link,
	Metadata,
	Property,
)
from itsor.domain.models.oscal.implementation.compenent import InventoryItem, SystemComponent, SystemId


class LocalDefinitions(OscalBaseModel):
	components: list[SystemComponent] | None = None
	inventory_items: list[InventoryItem] | None = Field(default=None, alias="inventory-items")
	assessment_assets: AssessmentAssets | None = Field(default=None, alias="assessment-assets")
	remarks: str | None = None


class RelatedFinding(OscalBaseModel):
	finding_uuid: UUID = Field(alias="finding-uuid")
	remarks: str | None = None


class PoamItem(OscalBaseModel):
	id: OscalPoamItemId = field(default_factory=typed_ulid_factory(OscalPoamItemId), init=False)
	title: str
	description: str
	uuid: UUID | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	origins: list[Origin] | None = None
	related_findings: list[RelatedFinding] | None = Field(default=None, alias="related-findings")
	related_observations: list[RelatedObservation] | None = Field(default=None, alias="related-observations")
	related_risks: list[AssociatedRisk] | None = Field(default=None, alias="related-risks")
	remarks: str | None = None


class PlanOfActionAndMilestones(OscalBaseModel):
	id: OscalPoamId = field(default_factory=typed_ulid_factory(OscalPoamId), init=False)
	uuid: UUID
	metadata: Metadata
	poam_items: list[PoamItem] = Field(alias="poam-items", min_length=1)
	import_ssp: ImportSsp | None = Field(default=None, alias="import-ssp")
	system_id: SystemId | None = Field(default=None, alias="system-id")
	local_definitions: LocalDefinitions | None = Field(default=None, alias="local-definitions")
	observations: list[Observation] | None = None
	risks: list[Risk] | None = None
	findings: list[Finding] | None = None
	back_matter: BackMatter | None = Field(default=None, alias="back-matter")


class OscalPoamDocument(OscalBaseModel):
	schema_directive: str | None = Field(default=None, alias="$schema")
	plan_of_action_and_milestones: PlanOfActionAndMilestones = Field(alias="plan-of-action-and-milestones")


__all__ = [
	"LocalDefinitions",
	"OscalPoamDocument",
	"PlanOfActionAndMilestones",
	"PoamItem",
]
