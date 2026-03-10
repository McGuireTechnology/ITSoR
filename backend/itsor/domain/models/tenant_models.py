from dataclasses import dataclass, field

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids import GroupId, TenantId, UserId


def _normalize_required_text(value: str, field_name: str) -> str:
	if not isinstance(value, str):
		raise ValueError(f"{field_name} must be a string")
	normalized = value.strip()
	if not normalized:
		raise ValueError(f"{field_name} is required")
	return normalized


@dataclass
class Tenant:
	id: TenantId = field(default_factory=typed_ulid_factory(TenantId), init=False)
	name: str
	owner_id: UserId | None = None
	group_id: GroupId | None = None
	permissions: int | None = None

	def __post_init__(self) -> None:
		self.name = _normalize_required_text(self.name, "name")


__all__ = ["Tenant"]

