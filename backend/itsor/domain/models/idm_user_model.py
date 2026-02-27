from dataclasses import dataclass, field

from itsor.domain.ids import generate_ulid


@dataclass
class IdmUser:
    id: str = field(default_factory=generate_ulid)
    person_id: str = ""
    username: str = ""
    account_status: str = "active"
