from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids import (
	AppId,
	MenuViewId,
	NavigationItemId,
	ResourceId,
	TableId,
	TenantId,
	ViewId,
)


class ViewType(str, Enum):
	LIST = "list"
	DETAIL = "detail"
	FORM = "form"
	BOARD = "board"
	CALENDAR = "calendar"
	DASHBOARD = "dashboard"


class ItemType(str, Enum):
	ROUTE = "route"
	RECORD = "record"
	ACTION = "action"


class AppViewType(str, Enum):
	TABLE = "table"
	FORM = "form"
	DETAIL = "detail"
	CARD = "card"
	DECK = "deck"
	GALLERY = "gallery"
	DASHBOARD = "dashboard"
	MAP = "map"


@dataclass
class NavigationItem:
	id: NavigationItemId = field(default_factory=typed_ulid_factory(NavigationItemId), init=False)
	label: str
	item_type: ItemType
	route: str
	resource_id: ResourceId
	icon: str | None = None
	order: int = 0
	metadata: dict[str, str] = field(default_factory=dict)

	def __post_init__(self) -> None:
		self.label = self.label.strip()
		self.route = self.route.strip()

		if not self.label:
			raise ValueError("Navigation item label cannot be empty")

		if not self.route:
			raise ValueError("Navigation item route cannot be empty")

		if self.order < 0:
			raise ValueError("Navigation item order cannot be negative")


@dataclass
class NavigationView:
	id: MenuViewId = field(default_factory=typed_ulid_factory(MenuViewId), init=False)
	key: str
	label: str
	view_type: ViewType
	route: str
	resource_id: ResourceId
	tenant_id: TenantId | None = None
	source_id: MenuViewId | None = None
	icon: str | None = None
	order: int = 0
	enabled: bool = True
	items: list[NavigationItem] = field(default_factory=list)

	def __post_init__(self) -> None:
		self.key = self.key.strip()
		self.label = self.label.strip()
		self.route = self.route.strip()

		if not self.key:
			raise ValueError("Navigation view key cannot be empty")

		if not self.label:
			raise ValueError("Navigation view label cannot be empty")

		if not self.route:
			raise ValueError("Navigation view route cannot be empty")

		if self.order < 0:
			raise ValueError("Navigation view order cannot be negative")


@dataclass
class AppView:
	id: ViewId = field(default_factory=typed_ulid_factory(ViewId), init=False)
	app_id: AppId
	name: str
	type: AppViewType
	table_id: TableId | None = None
	position: int = 0
	icon: str | None = None

	def __post_init__(self) -> None:
		self.name = self.name.strip()
		if not self.name:
			raise ValueError("View name cannot be empty")
		if self.position < 0:
			raise ValueError("View position cannot be negative")


__all__ = [
	"AppView",
	"AppViewType",
	"ItemType",
	"NavigationItem",
	"NavigationView",
	"ViewType",
]
