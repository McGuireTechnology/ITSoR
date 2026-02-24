from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class User:
    email: str
    password_hash: str
    id: UUID = field(default_factory=uuid4)
