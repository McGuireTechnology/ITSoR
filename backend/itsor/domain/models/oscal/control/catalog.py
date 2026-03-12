from __future__ import annotations

from dataclasses import field
from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import Field

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids.oscal import OscalCatalogId
from itsor.domain.models.oscal.base import OscalBaseModel, OscalEmptyObject


class Property(OscalBaseModel):
	name: str
	value: str
	uuid: UUID | None = None
	ns: str | None = None
	class_: str | None = Field(default=None, alias="class")
	group: str | None = None
	remarks: str | None = None


class Link(OscalBaseModel):
	href: str
	rel: str | None = None
	media_type: str | None = Field(default=None, alias="media-type")
	resource_fragment: str | None = Field(default=None, alias="resource-fragment")
	text: str | None = None


class Hash(OscalBaseModel):
	algorithm: Literal[
		"SHA-224",
		"SHA-256",
		"SHA-384",
		"SHA-512",
		"SHA3-224",
		"SHA3-256",
		"SHA3-384",
		"SHA3-512",
	] | str
	value: str


class DocumentIdentifier(OscalBaseModel):
	identifier: str
	scheme: str | None = None


class TelephoneNumber(OscalBaseModel):
	number: str
	type: Literal["home", "office", "mobile"] | str | None = None


class Address(OscalBaseModel):
	type: Literal["home", "work"] | str | None = None
	addr_lines: list[str] | None = Field(default=None, alias="addr-lines")
	city: str | None = None
	state: str | None = None
	postal_code: str | None = Field(default=None, alias="postal-code")
	country: str | None = None


class Role(OscalBaseModel):
	id: str
	title: str
	short_name: str | None = Field(default=None, alias="short-name")
	description: str | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class PartyExternalIdentifier(OscalBaseModel):
	id: str
	scheme: str


class Party(OscalBaseModel):
	uuid: UUID
	type: Literal["person", "organization"]
	name: str | None = None
	short_name: str | None = Field(default=None, alias="short-name")
	external_ids: list[PartyExternalIdentifier] | None = Field(default=None, alias="external-ids")
	props: list[Property] | None = None
	links: list[Link] | None = None
	email_addresses: list[str] | None = Field(default=None, alias="email-addresses")
	telephone_numbers: list[TelephoneNumber] | None = Field(default=None, alias="telephone-numbers")
	addresses: list[Address] | None = None
	location_uuids: list[UUID] | None = Field(default=None, alias="location-uuids")
	member_of_organizations: list[UUID] | None = Field(default=None, alias="member-of-organizations")
	remarks: str | None = None


class ResponsibleParty(OscalBaseModel):
	role_id: str = Field(alias="role-id")
	party_uuids: list[UUID] = Field(alias="party-uuids", min_length=1)
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class Action(OscalBaseModel):
	uuid: UUID
	type: str
	system: str
	date: datetime | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	responsible_parties: list[ResponsibleParty] | None = Field(
		default=None,
		alias="responsible-parties",
	)
	remarks: str | None = None


class RevisionEntry(OscalBaseModel):
	version: str
	title: str | None = None
	published: datetime | None = None
	last_modified: datetime | None = Field(default=None, alias="last-modified")
	oscal_version: str | None = Field(default=None, alias="oscal-version")
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class Location(OscalBaseModel):
	uuid: UUID
	title: str | None = None
	address: Address | None = None
	email_addresses: list[str] | None = Field(default=None, alias="email-addresses")
	telephone_numbers: list[TelephoneNumber] | None = Field(default=None, alias="telephone-numbers")
	urls: list[str] | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	remarks: str | None = None


class Citation(OscalBaseModel):
	text: str
	props: list[Property] | None = None
	links: list[Link] | None = None


class ResourceLink(OscalBaseModel):
	href: str
	media_type: str | None = Field(default=None, alias="media-type")
	hashes: list[Hash] | None = None


class ResourceBase64(OscalBaseModel):
	value: str
	filename: str | None = None
	media_type: str | None = Field(default=None, alias="media-type")


class Resource(OscalBaseModel):
	uuid: UUID
	title: str | None = None
	description: str | None = None
	props: list[Property] | None = None
	document_ids: list[DocumentIdentifier] | None = Field(default=None, alias="document-ids")
	citation: Citation | None = None
	rlinks: list[ResourceLink] | None = None
	base64: ResourceBase64 | None = None
	remarks: str | None = None


class BackMatter(OscalBaseModel):
	resources: list[Resource] | None = None


class Metadata(OscalBaseModel):
	title: str
	last_modified: datetime = Field(alias="last-modified")
	version: str
	oscal_version: str = Field(alias="oscal-version")
	published: datetime | None = None
	revisions: list[RevisionEntry] | None = None
	document_ids: list[DocumentIdentifier] | None = Field(default=None, alias="document-ids")
	props: list[Property] | None = None
	links: list[Link] | None = None
	roles: list[Role] | None = None
	locations: list[Location] | None = None
	parties: list[Party] | None = None
	responsible_parties: list[ResponsibleParty] | None = Field(
		default=None,
		alias="responsible-parties",
	)
	actions: list[Action] | None = None
	remarks: str | None = None


class ParameterConstraintTest(OscalBaseModel):
	expression: str
	remarks: str | None = None


class ParameterConstraint(OscalBaseModel):
	description: str | None = None
	tests: list[ParameterConstraintTest] | None = None


class ParameterGuideline(OscalBaseModel):
	prose: str


class ParameterSelection(OscalBaseModel):
	how_many: Literal["one", "one-or-more"] | None = Field(default=None, alias="how-many")
	choice: list[str] | None = None


class Parameter(OscalBaseModel):
	id: str | None = None
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
	remarks: str | None = None


class Part(OscalBaseModel):
	name: str
	id: str | None = None
	ns: str | None = None
	class_: str | None = Field(default=None, alias="class")
	title: str | None = None
	props: list[Property] | None = None
	prose: str | None = None
	parts: list[Part] | None = None
	links: list[Link] | None = None


class Control(OscalBaseModel):
	id: str
	title: str
	class_: str | None = Field(default=None, alias="class")
	params: list[Parameter] | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	parts: list[Part] | None = None
	controls: list[Control] | None = None


class Group(OscalBaseModel):
	title: str
	id: str | None = None
	class_: str | None = Field(default=None, alias="class")
	params: list[Parameter] | None = None
	props: list[Property] | None = None
	links: list[Link] | None = None
	parts: list[Part] | None = None
	groups: list[Group] | None = None
	controls: list[Control] | None = None


class Catalog(OscalBaseModel):
	id: OscalCatalogId = field(default_factory=typed_ulid_factory(OscalCatalogId), init=False)
	uuid: UUID
	metadata: Metadata
	params: list[Parameter] | None = None
	controls: list[Control] | None = None
	groups: list[Group] | None = None
	back_matter: BackMatter | None = Field(default=None, alias="back-matter")


class OscalCatalogDocument(OscalBaseModel):
	schema_directive: str | None = Field(default=None, alias="$schema")
	catalog: Catalog

__all__ = [
	"Action",
	"Address",
	"BackMatter",
	"Catalog",
	"Control",
	"DocumentIdentifier",
	"Group",
	"Hash",
	"Link",
	"Location",
	"Metadata",
	"OscalCatalogDocument",
	"OscalEmptyObject",
	"Parameter",
	"ParameterConstraint",
	"ParameterGuideline",
	"ParameterSelection",
	"Part",
	"Party",
	"Property",
	"ResponsibleParty",
]
