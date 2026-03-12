from __future__ import annotations

from dataclasses import field
from typing import Literal
from uuid import UUID

from pydantic import Field, model_validator

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids.oscal import OscalProfileId
from itsor.domain.models.oscal.base import OscalBaseModel, OscalEmptyObject
from itsor.domain.models.oscal.common import IncludeAll
from itsor.domain.models.oscal.control.catalog import (
	BackMatter,
	Link,
	Metadata,
	Parameter,
	ParameterConstraint,
	ParameterGuideline,
	ParameterSelection,
	Part,
	Property,
)


class Matching(OscalBaseModel):
	pattern: str
	remarks: str | None = None


class SelectControlById(OscalBaseModel):
	with_child_controls: Literal["yes", "no"] | None = Field(
		default=None,
		alias="with-child-controls",
	)
	with_ids: list[str] | None = Field(default=None, alias="with-ids")
	matching: list[Matching] | None = None


class ImportResource(OscalBaseModel):
	href: str | None = None
	include_all: IncludeAll | None = Field(default=None, alias="include-all")
	include_controls: list[SelectControlById] | None = Field(default=None, alias="include-controls")
	exclude_controls: list[SelectControlById] | None = Field(default=None, alias="exclude-controls")

	@model_validator(mode="after")
	def _validate_selection_mode(self) -> ImportResource:
		has_all = self.include_all is not None
		has_specific = bool(self.include_controls)
		if has_all == has_specific:
			raise ValueError("exactly one of include-all or include-controls must be provided")
		return self


class InsertControls(OscalBaseModel):
	order: Literal["keep", "ascending", "descending"] | None = None
	include_all: IncludeAll | None = Field(default=None, alias="include-all")
	include_controls: list[SelectControlById] | None = Field(default=None, alias="include-controls")
	exclude_controls: list[SelectControlById] | None = Field(default=None, alias="exclude-controls")

	@model_validator(mode="after")
	def _validate_insert_mode(self) -> InsertControls:
		has_all = self.include_all is not None
		has_specific = bool(self.include_controls)
		if has_all == has_specific:
			raise ValueError("exactly one of include-all or include-controls must be provided")
		return self


class Group(OscalBaseModel):
	title: str
	id: str | None = None
	class_: str | None = Field(default=None, alias="class")
	params: list[Parameter] | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	parts: list[Part] | None = None
	groups: list[Group] | None = None
	insert_controls: list[InsertControls] | None = Field(default=None, alias="insert-controls")


class MergeCustom(OscalBaseModel):
	groups: list[Group] | None = None
	insert_controls: list[InsertControls] | None = Field(default=None, alias="insert-controls")


class Merge(OscalBaseModel):
	combine: OscalEmptyObject | None = None
	flat: OscalEmptyObject | None = None
	as_is: bool | None = Field(default=None, alias="as-is")
	custom: MergeCustom | None = None

	@model_validator(mode="after")
	def _validate_merge_shape(self) -> Merge:
		selected = [self.flat is not None, self.as_is is not None, self.custom is not None]
		if sum(selected) != 1:
			raise ValueError("exactly one of flat, as-is, or custom must be provided")
		return self


class ParameterSetting(OscalBaseModel):
	param_id: str | None = Field(default=None, alias="param-id")
	class_: str | None = Field(default=None, alias="class")
	depends_on: str | None = Field(default=None, alias="depends-on")
	props: list[Property] | None = None
	links: list[Link] | None = None
	label: str | None = None
	usage: str | None = None
	constraints: list[ParameterConstraint] | None = None
	guidelines: list[ParameterGuideline] | None = None
	values: list[str] | None = None
	select: ParameterSelection | None = None


class Removal(OscalBaseModel):
	by_name: str | None = Field(default=None, alias="by-name")
	by_class: str | None = Field(default=None, alias="by-class")
	by_id: str | None = Field(default=None, alias="by-id")
	by_item_name: Literal["param", "prop", "link", "part", "mapping", "map"] | None = Field(
		default=None,
		alias="by-item-name",
	)
	by_ns: str | None = Field(default=None, alias="by-ns")
	remarks: str | None = None


class Addition(OscalBaseModel):
	position: Literal["before", "after", "starting", "ending"] | None = None
	by_id: str | None = Field(default=None, alias="by-id")
	title: str | None = None
	params: list[Parameter] | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	parts: list[Part] | None = None


class Alteration(OscalBaseModel):
	control_id: str = Field(alias="control-id")
	removes: list[Removal] | None = None
	adds: list[Addition] | None = None


class Modify(OscalBaseModel):
	set_parameters: list[ParameterSetting] | None = Field(default=None, alias="set-parameters")
	alters: list[Alteration] | None = None


class Profile(OscalBaseModel):
	id: OscalProfileId = field(default_factory=typed_ulid_factory(OscalProfileId), init=False)
	uuid: UUID
	metadata: Metadata
	imports: list[ImportResource] = Field(min_length=1)
	merge: Merge | None = None
	modify: Modify | None = None
	back_matter: BackMatter | None = Field(default=None, alias="back-matter")


class OscalProfileDocument(OscalBaseModel):
	schema_directive: str | None = Field(default=None, alias="$schema")
	profile: Profile

__all__ = [
	"Addition",
	"Alteration",
	"Group",
	"ImportResource",
	"IncludeAll",
	"InsertControls",
	"Matching",
	"Merge",
	"Modify",
	"OscalProfileDocument",
	"Profile",
	"Removal",
	"SelectControlById",
]
