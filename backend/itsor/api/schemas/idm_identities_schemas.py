from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class IdmIdentityCreate(BaseModel):
    person_id: str
    source_system: str
    source_record_id: str
    demographic_payload: dict[str, Any] = Field(default_factory=dict)
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    superseded_at: datetime | None = None


class IdmIdentityUpdate(BaseModel):
    source_system: str | None = None
    source_record_id: str | None = None
    demographic_payload: dict[str, Any] | None = None
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    superseded_at: datetime | None = None


class IdmIdentityResponse(BaseModel):
    id: str
    person_id: str
    source_system: str
    source_record_id: str
    demographic_payload: dict[str, Any] = Field(default_factory=dict)
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    superseded_at: datetime | None = None
