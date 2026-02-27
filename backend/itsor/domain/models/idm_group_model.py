from dataclasses import dataclass, field

from itsor.domain.ids import generate_ulid


@dataclass
class IdmGroup:
    id: str = field(default_factory=generate_ulid)
    name: str = ""
    description: str = ""
