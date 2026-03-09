from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

import ulid

from itsor.domain.ids import AppId, UserId


@dataclass
class App:
	id: AppId = field(default_factory=lambda: AppId(str(ulid.new())), init=False)
	name: str
	owner_id: UserId
	description: str | None = None
	created_at: datetime = field(default_factory=lambda: datetime.now(UTC), init=False)

	def __post_init__(self) -> None:
		if not self.name.strip():
			raise ValueError("App name cannot be empty")


__all__ = ["App"]