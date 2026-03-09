from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import ulid

from itsor.domain.ids import AppId, TableId, ViewId


class ViewType(str, Enum):
	TABLE = "table"
	FORM = "form"
	DETAIL = "detail"
	CARD = "card"
	DECK = "deck"
	GALLERY = "gallery"
	DASHBOARD = "dashboard"
	MAP = "map"


@dataclass
class View:
	id: ViewId = field(default_factory=lambda: ViewId(str(ulid.new())), init=False)
	app_id: AppId
	name: str
	type: ViewType
	table_id: TableId | None = None
	position: int = 0
	icon: str | None = None

	def __post_init__(self) -> None:
		if not self.name.strip():
			raise ValueError("View name cannot be empty")
		if self.position < 0:
			raise ValueError("View position cannot be negative")


__all__ = ["View", "ViewType"]