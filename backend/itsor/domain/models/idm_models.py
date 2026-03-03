from dataclasses import dataclass, field
from datetime import datetime
import ulid


@dataclass
class IdmGroupMembership:
    id: str = field(default_factory=generate_ulid)
    group_id: str = ""
    member_type: str = "user"
    member_user_id: str | None = None
    member_group_id: str | None = None


@dataclass
class IdmGroup:
    id: str = field(default_factory=generate_ulid)
    name: str = ""
    description: str = ""


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


@dataclass
class IdmPerson:
    id: str = field(default_factory=generate_ulid)
    display_name: str = ""
    current_identity_id: str | None = None


@dataclass
class IdmUser:
    id: str = field(default_factory=generate_ulid)
    person_id: str = ""
    username: str = ""
    account_status: str = "active"