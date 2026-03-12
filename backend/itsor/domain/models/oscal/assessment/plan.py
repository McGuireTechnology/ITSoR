from __future__ import annotations

from dataclasses import field
from typing import Literal
from uuid import UUID

from pydantic import Field, model_validator

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids.oscal import OscalAssessmentPlanId
from itsor.domain.models.oscal.base import OscalBaseModel, OscalEmptyObject
from itsor.domain.models.oscal.common import ResponsibleRole
from itsor.domain.models.oscal.control.catalog import (
	BackMatter,
	Link,
	Metadata,
	Part,
	Property,
	ResponsibleParty,
)
from itsor.domain.models.oscal.implementation.compenent import (
	InventoryItem,
	SystemComponent,
	SystemUser,
)


class ImportSsp(OscalBaseModel):
	href: str
	remarks: str | None = None


class SelectControlById(OscalBaseModel):
	control_id: str = Field(alias="control-id")
	statement_ids: list[str] | None = Field(default=None, alias="statement-ids")


class SelectObjectiveById(OscalBaseModel):
	objective_id: str = Field(alias="objective-id")
	remarks: str | None = None


class ControlSelection(OscalBaseModel):
	include_all: OscalEmptyObject | None = Field(default=None, alias="include-all")
	include_controls: list[SelectControlById] | None = Field(default=None, alias="include-controls")
	exclude_controls: list[SelectControlById] | None = Field(default=None, alias="exclude-controls")
	description: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None

	@model_validator(mode="after")
	def _validate_include_mode(self) -> ControlSelection:
		has_all = self.include_all is not None
		has_specific = bool(self.include_controls)
		if has_all == has_specific:
			raise ValueError("exactly one of include-all or include-controls must be provided")
		return self


class ControlObjectiveSelection(OscalBaseModel):
	include_all: OscalEmptyObject | None = Field(default=None, alias="include-all")
	include_objectives: list[SelectObjectiveById] | None = Field(default=None, alias="include-objectives")
	exclude_objectives: list[SelectObjectiveById] | None = Field(default=None, alias="exclude-objectives")
	description: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None

	@model_validator(mode="after")
	def _validate_include_mode(self) -> ControlObjectiveSelection:
		has_all = self.include_all is not None
		has_specific = bool(self.include_objectives)
		if has_all == has_specific:
			raise ValueError("exactly one of include-all or include-objectives must be provided")
		return self


class ReviewedControls(OscalBaseModel):
	control_selections: list[ControlSelection] = Field(alias="control-selections", min_length=1)
	control_objective_selections: list[ControlObjectiveSelection] | None = Field(
		default=None,
		alias="control-objective-selections",
	)
	description: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class LocalObjective(OscalBaseModel):
	control_id: str = Field(alias="control-id")
	parts: list[Part] = Field(min_length=1)
	description: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class ActivityStep(OscalBaseModel):
	uuid: UUID
	description: str
	title: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class Activity(OscalBaseModel):
	uuid: UUID
	description: str
	title: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	steps: list[ActivityStep] | None = None
	responsible_roles: list[ResponsibleRole] | None = Field(default=None, alias="responsible-roles")
	remarks: str | None = None


class LocalDefinitions(OscalBaseModel):
	components: list[SystemComponent] | None = None
	inventory_items: list[InventoryItem] | None = Field(default=None, alias="inventory-items")
	users: list[SystemUser] | None = None
	objectives_and_methods: list[LocalObjective] | None = Field(default=None, alias="objectives-and-methods")
	activities: list[Activity] | None = None
	remarks: str | None = None


class TermsAndConditions(OscalBaseModel):
 	parts: list[Part] = Field(min_length=1)


class SelectSubjectById(OscalBaseModel):
	subject_uuid: UUID = Field(alias="subject-uuid")
	type: Literal["component", "inventory-item", "location", "party", "user", "resource"] | str
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class AssessmentSubject(OscalBaseModel):
	type: Literal["component", "inventory-item", "location", "party", "user"] | str | None = None
	include_all: OscalEmptyObject | None = Field(default=None, alias="include-all")
	include_subjects: list[SelectSubjectById] | None = Field(default=None, alias="include-subjects")
	exclude_subjects: list[SelectSubjectById] | None = Field(default=None, alias="exclude-subjects")
	description: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None

	@model_validator(mode="after")
	def _validate_subject_scope(self) -> AssessmentSubject:
		has_all = self.include_all is not None
		has_specific = bool(self.include_subjects)
		if has_all == has_specific:
			raise ValueError("exactly one of include-all or include-subjects must be provided")
		return self


class UsesComponent(OscalBaseModel):
	component_uuid: UUID = Field(alias="component-uuid")
	props: list[Property] | None = None
	links: list[Link] | None = None
	responsible_parties: list[ResponsibleParty] | None = Field(default=None, alias="responsible-parties")
	remarks: str | None = None


class AssessmentPlatform(OscalBaseModel):
	uuid: UUID
	title: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	uses_components: list[UsesComponent] | None = Field(default=None, alias="uses-components")
	remarks: str | None = None


class AssessmentAssets(OscalBaseModel):
	components: list[SystemComponent] | None = None
	assessment_platforms: list[AssessmentPlatform] = Field(alias="assessment-platforms", min_length=1)


class TimingOnDate(OscalBaseModel):
	date: str
	remarks: str | None = None


class TimingWithinDateRange(OscalBaseModel):
	start: str
	end: str
	remarks: str | None = None


class TimingAtFrequency(OscalBaseModel):
	period: int
	unit: Literal["seconds", "minutes", "hours", "days", "months", "years"] | str
	remarks: str | None = None


class TaskTiming(OscalBaseModel):
	on_date: TimingOnDate | None = Field(default=None, alias="on-date")
	within_date_range: TimingWithinDateRange | None = Field(default=None, alias="within-date-range")
	at_frequency: TimingAtFrequency | None = Field(default=None, alias="at-frequency")

	@model_validator(mode="after")
	def _validate_timing_mode(self) -> TaskTiming:
		selected = [
			self.on_date is not None,
			self.within_date_range is not None,
			self.at_frequency is not None,
		]
		if sum(selected) != 1:
			raise ValueError("exactly one of on-date, within-date-range, or at-frequency must be provided")
		return self


class TaskDependency(OscalBaseModel):
	task_uuid: UUID = Field(alias="task-uuid")
	remarks: str | None = None


class AssociatedActivity(OscalBaseModel):
	activity_uuid: UUID = Field(alias="activity-uuid")
	subjects: list[AssessmentSubject] = Field(min_length=1)
	props: list[Property] | None = None
	links: list[Link] | None = None
	responsible_roles: list[ResponsibleRole] | None = Field(default=None, alias="responsible-roles")
	remarks: str | None = None


class Task(OscalBaseModel):
	uuid: UUID
	type: str
	title: str
	description: str | None = None
	timing: TaskTiming | None = None
	dependencies: list[TaskDependency] | None = None
	tasks: list[Task] | None = None
	associated_activities: list[AssociatedActivity] | None = Field(default=None, alias="associated-activities")
	subjects: list[AssessmentSubject] | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	responsible_roles: list[ResponsibleRole] | None = Field(default=None, alias="responsible-roles")
	remarks: str | None = None


class AssessmentPlan(OscalBaseModel):
	id: OscalAssessmentPlanId = field(default_factory=typed_ulid_factory(OscalAssessmentPlanId), init=False)
	uuid: UUID
	metadata: Metadata
	import_ssp: ImportSsp = Field(alias="import-ssp")
	reviewed_controls: ReviewedControls = Field(alias="reviewed-controls")
	assessment_subjects: list[AssessmentSubject] | None = Field(default=None, alias="assessment-subjects")
	assessment_assets: AssessmentAssets | None = Field(default=None, alias="assessment-assets")
	tasks: list[Task] | None = None
	local_definitions: LocalDefinitions | None = Field(default=None, alias="local-definitions")
	terms_and_conditions: TermsAndConditions | None = Field(default=None, alias="terms-and-conditions")
	back_matter: BackMatter | None = Field(default=None, alias="back-matter")


class OscalAssessmentPlanDocument(OscalBaseModel):
	schema_directive: str | None = Field(default=None, alias="$schema")
	assessment_plan: AssessmentPlan = Field(alias="assessment-plan")

__all__ = [
	"Activity",
	"ActivityStep",
	"AssociatedActivity",
	"AssessmentAssets",
	"AssessmentPlan",
	"AssessmentPlatform",
	"AssessmentSubject",
	"ControlObjectiveSelection",
	"ControlSelection",
	"ImportSsp",
	"LocalDefinitions",
	"LocalObjective",
	"OscalAssessmentPlanDocument",
	"ReviewedControls",
	"SelectControlById",
	"SelectObjectiveById",
	"SelectSubjectById",
	"Task",
	"TaskTiming",
]
