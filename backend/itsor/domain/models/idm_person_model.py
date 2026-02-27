from dataclasses import dataclass, field

from itsor.domain.ids import generate_ulid


@dataclass
class IdmPerson:
    id: str = field(default_factory=generate_ulid)
    display_name: str = ""
    current_identity_id: str | None = None
