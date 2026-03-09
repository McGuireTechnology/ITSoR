from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import ulid

from itsor.domain.ids import AppId, AppUserId, UserId


class AppRole(str, Enum):
	OWNER = "owner"
	EDITOR = "editor"
	USER = "user"
	READ_ONLY = "read_only"


@dataclass
class AppUser:
	id: AppUserId = field(default_factory=lambda: AppUserId(str(ulid.new())), init=False)
	app_id: AppId
	user_id: UserId
	role: AppRole


__all__ = ["AppRole", "AppUser"]