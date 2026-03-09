from dataclasses import dataclass, field

import ulid

from itsor.domain.ids import GroupId, TenantId, UserId


@dataclass
class Tenant:
	id: TenantId = field(default_factory=lambda: TenantId(str(ulid.new())), init=False)
	name: str
	owner_id: UserId | None = None
	group_id: GroupId | None = None
	permissions: int | None = None


__all__ = ["Tenant"]

