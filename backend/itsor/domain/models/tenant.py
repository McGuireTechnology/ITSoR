from dataclasses import dataclass, field

from itsor.domain.ids import generate_ulid


@dataclass
class Tenant:
    name: str
    id: str = field(default_factory=generate_ulid)
