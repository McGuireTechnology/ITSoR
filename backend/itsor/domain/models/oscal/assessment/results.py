from __future__ import annotations

from dataclasses import field
from typing import Literal
from uuid import UUID

from pydantic import Field

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids.oscal import OscalAssessmentResultId, OscalAssessmentResultsId
from itsor.domain.models.oscal.base import OscalBaseModel
from itsor.domain.models.oscal.assessment.plan import (
	Activity,
	AssessmentAssets,
	AssessmentSubject,
	LocalObjective,
	ReviewedControls,
	Task,
)
from itsor.domain.models.oscal.control.catalog import (
	BackMatter,
	Link,
	Metadata,
	Part,
	Property,
	ResponsibleParty,
)
from itsor.domain.models.oscal.implementation.compenent import (
	ImplementationStatus,
	InventoryItem,
	SystemComponent,
	SystemUser,
)


class ImportAp(OscalBaseModel):
	href: str
	remarks: str | None = None


class AssessmentResultsLocalDefinitions(OscalBaseModel):
	objectives_and_methods: list[LocalObjective] | None = Field(default=None, alias="objectives-and-methods")
	activities: list[Activity] | None = None
	remarks: str | None = None


class ResultLocalDefinitions(OscalBaseModel):
	components: list[SystemComponent] | None = None
	inventory_items: list[InventoryItem] | None = Field(default=None, alias="inventory-items")
	users: list[SystemUser] | None = None
	assessment_assets: AssessmentAssets | None = Field(default=None, alias="assessment-assets")
	tasks: list[Task] | None = None


class Attestation(OscalBaseModel):
	parts: list[Part] = Field(min_length=1)
	responsible_parties: list[ResponsibleParty] | None = Field(default=None, alias="responsible-parties")


class LoggedBy(OscalBaseModel):
	party_uuid: UUID = Field(alias="party-uuid")
	role_id: str | None = Field(default=None, alias="role-id")
	remarks: str | None = None


class RelatedTask(OscalBaseModel):
	task_uuid: UUID = Field(alias="task-uuid")
	props: list[Property] | None = None
	links: list[Link] | None = None
	responsible_parties: list[ResponsibleParty] | None = Field(default=None, alias="responsible-parties")
	subjects: list[AssessmentSubject] | None = None
	remarks: str | None = None


class AssessmentLogEntry(OscalBaseModel):
	uuid: UUID
	start: str
	title: str | None = None
	description: str | None = None
	end: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	logged_by: list[LoggedBy] | None = Field(default=None, alias="logged-by")
	related_tasks: list[RelatedTask] | None = Field(default=None, alias="related-tasks")
	remarks: str | None = None


class AssessmentLog(OscalBaseModel):
	entries: list[AssessmentLogEntry] = Field(min_length=1)


class OriginActor(OscalBaseModel):
	type: Literal["tool", "assessment-platform", "party"]
	actor_uuid: UUID = Field(alias="actor-uuid")
	role_id: str | None = Field(default=None, alias="role-id")
	props: list[Property] | None = None
	links: list[Link] | None = None


class Origin(OscalBaseModel):
	actors: list[OriginActor] = Field(min_length=1)
	related_tasks: list[RelatedTask] | None = Field(default=None, alias="related-tasks")


class SubjectReference(OscalBaseModel):
	subject_uuid: UUID = Field(alias="subject-uuid")
	type: Literal["component", "inventory-item", "location", "party", "user", "resource"] | str
	title: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class RelevantEvidence(OscalBaseModel):
	description: str
	href: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class Observation(OscalBaseModel):
	uuid: UUID
	description: str
	methods: list[Literal["EXAMINE", "INTERVIEW", "TEST", "UNKNOWN"] | str] = Field(min_length=1)
	collected: str
	title: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	types: list[
		Literal[
			"ssp-statement-issue",
			"control-objective",
			"mitigation",
			"finding",
			"discovery",
			"historic",
		]
		| str
	] | None = None
	origins: list[Origin] | None = None
	subjects: list[SubjectReference] | None = None
	relevant_evidence: list[RelevantEvidence] | None = Field(default=None, alias="relevant-evidence")
	expires: str | None = None
	remarks: str | None = None


class RelatedObservation(OscalBaseModel):
	observation_uuid: UUID = Field(alias="observation-uuid")
	remarks: str | None = None


class AssociatedRisk(OscalBaseModel):
	risk_uuid: UUID = Field(alias="risk-uuid")
	remarks: str | None = None


class FindingTargetStatus(OscalBaseModel):
	state: Literal["satisfied", "not-satisfied"]
	reason: Literal["pass", "fail", "other"] | str | None = None
	remarks: str | None = None


class FindingTarget(OscalBaseModel):
	type: Literal["statement-id", "objective-id"]
	target_id: str = Field(alias="target-id")
	status: FindingTargetStatus
	title: str | None = None
	description: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	implementation_status: ImplementationStatus | None = Field(
		default=None,
		alias="implementation-status",
	)
	remarks: str | None = None


class Finding(OscalBaseModel):
	uuid: UUID
	title: str
	description: str
	target: FindingTarget
	props: list[Property] | None = None
	links: list[Link] | None = None
	origins: list[Origin] | None = None
	implementation_statement_uuid: UUID | None = Field(default=None, alias="implementation-statement-uuid")
	related_observations: list[RelatedObservation] | None = Field(default=None, alias="related-observations")
	related_risks: list[AssociatedRisk] | None = Field(default=None, alias="related-risks")
	remarks: str | None = None


RiskStatus = (
	Literal[
		"open",
		"investigating",
		"remediating",
		"deviation-requested",
		"deviation-approved",
		"closed",
	]
	| str
)


class ThreatId(OscalBaseModel):
	id: str
	system: str
	href: str | None = None


class Facet(OscalBaseModel):
	name: str
	system: str
	value: str
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class Characterization(OscalBaseModel):
	origin: Origin
	facets: list[Facet] = Field(min_length=1)
	props: list[Property] | None = None
	links: list[Link] | None = None


class RequiredAsset(OscalBaseModel):
	uuid: UUID
	description: str
	subjects: list[SubjectReference] | None = None
	title: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class Response(OscalBaseModel):
	uuid: UUID
	lifecycle: Literal["recommendation", "planned", "completed"] | str
	title: str
	description: str
	props: list[Property] | None = None
	links: list[Link] | None = None
	origins: list[Origin] | None = None
	required_assets: list[RequiredAsset] | None = Field(default=None, alias="required-assets")
	tasks: list[Task] | None = None
	remarks: str | None = None


class RiskLogRelatedResponse(OscalBaseModel):
	response_uuid: UUID = Field(alias="response-uuid")
	props: list[Property] | None = None
	links: list[Link] | None = None
	related_tasks: list[RelatedTask] | None = Field(default=None, alias="related-tasks")
	remarks: str | None = None


class RiskLogEntry(OscalBaseModel):
	uuid: UUID
	start: str
	title: str | None = None
	description: str | None = None
	end: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	logged_by: list[LoggedBy] | None = Field(default=None, alias="logged-by")
	status_change: RiskStatus | None = Field(default=None, alias="status-change")
	related_responses: list[RiskLogRelatedResponse] | None = Field(default=None, alias="related-responses")
	remarks: str | None = None


class RiskLog(OscalBaseModel):
	entries: list[RiskLogEntry] = Field(min_length=1)


class MitigatingFactor(OscalBaseModel):
	uuid: UUID
	description: str
	implementation_uuid: UUID | None = Field(default=None, alias="implementation-uuid")
	props: list[Property] | None = None
	links: list[Link] | None = None
	subjects: list[SubjectReference] | None = None


class Risk(OscalBaseModel):
	uuid: UUID
	title: str
	description: str
	statement: str
	status: RiskStatus
	props: list[Property] | None = None
	links: list[Link] | None = None
	origins: list[Origin] | None = None
	threat_ids: list[ThreatId] | None = Field(default=None, alias="threat-ids")
	characterizations: list[Characterization] | None = None
	mitigating_factors: list[MitigatingFactor] | None = Field(default=None, alias="mitigating-factors")
	deadline: str | None = None
	remediations: list[Response] | None = None
	risk_log: RiskLog | None = Field(default=None, alias="risk-log")
	related_observations: list[RelatedObservation] | None = Field(default=None, alias="related-observations")


class AssessmentResult(OscalBaseModel):
	id: OscalAssessmentResultId = field(default_factory=typed_ulid_factory(OscalAssessmentResultId), init=False)
	uuid: UUID
	title: str
	description: str
	start: str
	reviewed_controls: ReviewedControls = Field(alias="reviewed-controls")
	end: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	local_definitions: ResultLocalDefinitions | None = Field(default=None, alias="local-definitions")
	attestations: list[Attestation] | None = None
	assessment_log: AssessmentLog | None = Field(default=None, alias="assessment-log")
	observations: list[Observation] | None = None
	risks: list[Risk] | None = None
	findings: list[Finding] | None = None
	remarks: str | None = None


class AssessmentResults(OscalBaseModel):
	id: OscalAssessmentResultsId = field(default_factory=typed_ulid_factory(OscalAssessmentResultsId), init=False)
	uuid: UUID
	metadata: Metadata
	import_ap: ImportAp = Field(alias="import-ap")
	results: list[AssessmentResult] = Field(min_length=1)
	local_definitions: AssessmentResultsLocalDefinitions | None = Field(default=None, alias="local-definitions")
	back_matter: BackMatter | None = Field(default=None, alias="back-matter")


class OscalAssessmentResultsDocument(OscalBaseModel):
	schema_directive: str | None = Field(default=None, alias="$schema")
	assessment_results: AssessmentResults = Field(alias="assessment-results")


__all__ = [
	"AssessmentResult",
	"AssessmentResults",
	"ImportAp",
	"Observation",
	"OscalAssessmentResultsDocument",
	"Risk",
	"Finding",
]
