from dataclasses import dataclass, field

from itsor.domain.ids import generate_ulid


@dataclass
class User:
    id: str = field(default_factory=generate_ulid)
    name: str = ""
    group_id: str | None = None
    email: str = ""
    username: str = ""
    password_hash: str = ""
