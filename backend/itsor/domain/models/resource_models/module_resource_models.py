from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids import ModuleId, ResourceId, TenantId

if TYPE_CHECKING:
	from itsor.domain.models.view_models import NavigationView


def _navigation_view_list_factory() -> list[NavigationView]:
	return []


@dataclass
class ModuleResource:
	id: ResourceId = field(default_factory=typed_ulid_factory(ResourceId), init=False)
	key: str
	label: str
	module_id: ModuleId
	list_route: str
	tenant_id: TenantId | None = None
	source_id: ResourceId | None = None
	icon: str | None = None
	order: int = 0
	enabled: bool = True
	views: list[NavigationView] = field(default_factory=_navigation_view_list_factory)

	def __post_init__(self) -> None:
		self.key = self.key.strip()
		self.label = self.label.strip()
		self.list_route = self.list_route.strip()

		if not self.key:
			raise ValueError("Module resource key cannot be empty")

		if not self.label:
			raise ValueError("Module resource label cannot be empty")

		if not self.list_route:
			raise ValueError("Module resource list_route cannot be empty")

		if self.order < 0:
			raise ValueError("Module resource order cannot be negative")


__all__ = ["ModuleResource"]
