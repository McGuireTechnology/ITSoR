from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING
import warnings

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids import AppUserId, ModuleId, TenantId, UserId

if TYPE_CHECKING:
	from itsor.domain.models.resource_models import ModuleResource


class ModuleType(str, Enum):
	SYSTEM = "system"
	CUSTOM = "custom"
	APP = "app"


class ModuleRole(str, Enum):
	OWNER = "owner"
	EDITOR = "editor"
	USER = "user"
	READ_ONLY = "read_only"


@dataclass
class Module:
	id: ModuleId = field(default_factory=typed_ulid_factory(ModuleId), init=False)
	key: str
	label: str
	module_type: ModuleType = ModuleType.CUSTOM
	tenant_id: TenantId | None = None
	source_id: ModuleId | None = None
	icon: str | None = None
	order: int = 0
	enabled: bool = True
	resources: list[ModuleResource] = field(default_factory=list)

	def __post_init__(self) -> None:
		self.key = self.key.strip()
		self.label = self.label.strip()

		if not self.key:
			raise ValueError("Module key cannot be empty")

		if not self.label:
			raise ValueError("Module label cannot be empty")

		if self.order < 0:
			raise ValueError("Module order cannot be negative")


@dataclass
class ModuleUser:
	id: AppUserId = field(default_factory=typed_ulid_factory(AppUserId), init=False)
	module_id: ModuleId
	user_id: UserId
	role: ModuleRole


_DEPRECATED_ALIASES: dict[str, type[object]] = {
	"App": Module,
	"AppRole": ModuleRole,
	"AppUser": ModuleUser,
}


def __getattr__(name: str) -> type[object]:
	if name in _DEPRECATED_ALIASES:
		warnings.warn(
			f"`{name}` is deprecated and will be removed in a future release. Use `{_DEPRECATED_ALIASES[name].__name__}` instead.",
			DeprecationWarning,
			stacklevel=2,
		)
		return _DEPRECATED_ALIASES[name]
	raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
	"Module",
	"ModuleRole",
	"ModuleType",
	"ModuleUser",
]
