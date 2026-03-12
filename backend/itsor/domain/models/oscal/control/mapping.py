from __future__ import annotations

from dataclasses import field
from typing import Literal
from uuid import UUID

from pydantic import Field, model_validator

from itsor.domain.models.oscal.base import OscalBaseModel
from itsor.domain.models.oscal.control.catalog import (
	BackMatter,
	Link,
	Metadata,
	Property,
	ResponsibleParty,
)
from itsor.domain.models.oscal.control.profile import SelectControlById
from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids.oscal import OscalMappingCollectionId, OscalMappingId


class MappingResourceReference(OscalBaseModel):
	type: Literal["catalog", "profile"] | str
	href: str
	ns: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class Coverage(OscalBaseModel):
	target_coverage: float = Field(alias="target-coverage")
	generation_method: Literal["arbitrary"] | str | None = Field(
		default=None,
		alias="generation-method",
	)

	@model_validator(mode="after")
	def _validate_percentage(self) -> Coverage:
		if not 0.0 <= self.target_coverage <= 1.0:
			raise ValueError("target-coverage must be between 0 and 1")
		return self


class ConfidenceScore(OscalBaseModel):
	category: str | None = None
	percentage: float | None = None

	@model_validator(mode="after")
	def _validate_score(self) -> ConfidenceScore:
		has_category = self.category is not None
		has_percentage = self.percentage is not None
		if has_category == has_percentage:
			raise ValueError("exactly one of category or percentage must be provided")
		if self.percentage is not None and not 0.0 <= self.percentage <= 1.0:
			raise ValueError("percentage must be between 0 and 1")
		return self


class MappingItem(OscalBaseModel):
	type: Literal["control", "statement"]
	id_ref: str = Field(alias="id-ref")
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class QualifierItem(OscalBaseModel):
	subject: Literal["source", "target", "both"]
	predicate: Literal["has-requirement", "has-incompatibility"]
	category: Literal["restricted", "addressable", "blocked"]
	description: str
	remarks: str | None = None


class GapSummary(OscalBaseModel):
	uuid: UUID
	unmapped_controls: list[SelectControlById] = Field(alias="unmapped-controls", min_length=1)


class MappingEntry(OscalBaseModel):
	uuid: UUID
	relationship: str
	sources: list[MappingItem] = Field(min_length=1)
	targets: list[MappingItem] = Field(min_length=1)
	ns: str | None = None
	matching_rationale: Literal["syntactic", "semantic", "functional"] | None = Field(
		default=None,
		alias="matching-rationale",
	)
	qualifiers: list[QualifierItem] | None = None
	confidence_score: ConfidenceScore | None = Field(default=None, alias="confidence-score")
	coverage: Coverage | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class Mapping(OscalBaseModel):
	id: OscalMappingId = field(default_factory=typed_ulid_factory(OscalMappingId), init=False)
	uuid: UUID
	source_resource: MappingResourceReference = Field(alias="source-resource")
	target_resource: MappingResourceReference = Field(alias="target-resource")
	maps: list[MappingEntry] = Field(min_length=1)
	method: Literal["human", "automation", "hybrid"] | None = None
	matching_rationale: Literal["syntactic", "semantic", "functional"] | None = Field(
		default=None,
		alias="matching-rationale",
	)
	status: Literal["complete", "not-complete", "draft", "deprecated", "superseded"] | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None
	mapping_description: str | None = Field(default=None, alias="mapping-description")
	source_gap_summary: GapSummary | None = Field(default=None, alias="source-gap-summary")
	target_gap_summary: GapSummary | None = Field(default=None, alias="target-gap-summary")
	confidence_score: ConfidenceScore | None = Field(default=None, alias="confidence-score")
	coverage: Coverage | None = None


class MappingProvenance(OscalBaseModel):
	method: Literal["human", "automation", "hybrid"]
	matching_rationale: Literal["syntactic", "semantic", "functional"] = Field(
		alias="matching-rationale",
	)
	status: Literal["complete", "not-complete", "draft", "deprecated", "superseded"]
	mapping_description: str = Field(alias="mapping-description")
	confidence_score: ConfidenceScore | None = Field(default=None, alias="confidence-score")
	coverage: Coverage | None = None
	responsible_parties: list[ResponsibleParty] | None = Field(
		default=None,
		alias="responsible-parties",
	)
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class MappingCollection(OscalBaseModel):
	id: OscalMappingCollectionId = field(default_factory=typed_ulid_factory(OscalMappingCollectionId), init=False)
	uuid: UUID
	metadata: Metadata
	provenance: MappingProvenance
	mappings: Mapping | list[Mapping]
	back_matter: BackMatter | None = Field(default=None, alias="back-matter")


class OscalMappingDocument(OscalBaseModel):
	schema_directive: str | None = Field(default=None, alias="$schema")
	mapping_collection: MappingCollection = Field(alias="mapping-collection")


__all__ = [
	"ConfidenceScore",
	"Coverage",
	"GapSummary",
	"Mapping",
	"MappingCollection",
	"MappingEntry",
	"MappingItem",
	"MappingProvenance",
	"MappingResourceReference",
	"OscalMappingDocument",
	"QualifierItem",
]
