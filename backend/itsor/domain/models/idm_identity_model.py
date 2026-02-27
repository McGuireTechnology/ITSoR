from dataclasses import dataclass, field
from datetime import datetime

from itsor.domain.ids import generate_ulid


@dataclass
class IdmIdentity:
    id: str = field(default_factory=generate_ulid)
    person_id: str = ""
    source_system: str = ""
    source_record_id: str = ""
    demographic_payload: str = "{}"
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    superseded_at: datetime | None = None
