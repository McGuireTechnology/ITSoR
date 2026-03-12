from dataclasses import dataclass, field
from enum import Enum

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids import FrameworkId, DomainId, ControlId, ControlLinkId, ControlGuidanceId, ControlExampleId

@dataclass
class Framework:
	id: FrameworkId = field(default_factory=typed_ulid_factory(FrameworkId), init=False)
	name: str 
	version: str
	description: str

@dataclass
class Domain:
	id: DomainId = field(default_factory=typed_ulid_factory(DomainId), init=False)
	framework_id: FrameworkId
	name: str
	number: str
	description: str

@dataclass
class Control:
	id: ControlId = field(default_factory=typed_ulid_factory(ControlId), init=False)
	domain_id: DomainId
	name: str
	number: str
	description: str
	asset_class_id: str | None = None
	implementation_group_id: str | None = None
	frequency_id: str | None = None
	
class LinkType(str, Enum):
	REQUIRED = "required"
	REFERENCE = "reference"

@dataclass
class ImplementationGroup:
	id: str = field(default_factory=typed_ulid_factory(str), init=False)
	name: str
	description: str
	
@dataclass
class ControlLink:
	id: ControlLinkId = field(default_factory=typed_ulid_factory(ControlLinkId), init=False)
	link_type: LinkType
	control_id: ControlId
	required_control_id: ControlId
	resource_id: str

@dataclass
class ControlExample:
	id: ControlExampleId = field(default_factory=typed_ulid_factory(ControlExampleId), init=False)
	control_id: ControlId
	description: str


@dataclass
class ControlGuidance:
	id: ControlGuidanceId = field(default_factory=typed_ulid_factory(ControlGuidanceId), init=False)
	control_id: ControlId
	description: str


__all__ = ["Framework", "Domain", "Control", "LinkType", "ControlLink", "ControlExample", "ControlGuidance"]
