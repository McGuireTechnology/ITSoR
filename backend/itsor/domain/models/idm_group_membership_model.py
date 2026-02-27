from dataclasses import dataclass, field

from itsor.domain.ids import generate_ulid


@dataclass
class IdmGroupMembership:
    id: str = field(default_factory=generate_ulid)
    group_id: str = ""
    member_type: str = "user"
    member_user_id: str | None = None
    member_group_id: str | None = None
