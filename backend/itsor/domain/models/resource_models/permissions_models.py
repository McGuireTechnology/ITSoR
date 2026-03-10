from __future__ import annotations

from enum import Enum


class ResourcePermissionAction(str, Enum):
	CREATE = "create"
	READ = "read"
	UPDATE = "update"
	DELETE = "delete"
	EXECUTE = "execute"

	@classmethod
	def from_verb(cls, verb: str) -> ResourcePermissionAction:
		normalized = verb.strip().lower()
		if normalized in {"write", "modify"}:
			normalized = cls.UPDATE.value
		try:
			return cls(normalized)
		except ValueError as exc:
			raise ValueError(f"Unsupported action verb '{verb}'") from exc

	@classmethod
	def from_nibble(cls, value: int) -> ResourcePermissionAction:
		nibble_map = {
			0x1: cls.CREATE,
			0x2: cls.READ,
			0x4: cls.UPDATE,
			0x8: cls.DELETE,
			0x10: cls.EXECUTE,
		}
		try:
			return nibble_map[value]
		except KeyError as exc:
			raise ValueError(f"Unsupported action nibble '{value}'") from exc

	def to_nibble(self) -> int:
		nibble_map = {
			ResourcePermissionAction.CREATE: 0x1,
			ResourcePermissionAction.READ: 0x2,
			ResourcePermissionAction.UPDATE: 0x4,
			ResourcePermissionAction.DELETE: 0x8,
			ResourcePermissionAction.EXECUTE: 0x10,
		}
		return nibble_map[self]


class Resource(str, Enum):
	USER = "platform.user"
	TENANT = "platform.tenant"
	GROUP = "platform.group"
	ROLE = "platform.role"
	PERMISSION = "platform.permission"
	USER_TENANT = "platform.user_tenant"
	GROUP_MEMBERSHIP = "platform.group_membership"
	USER_ROLE = "platform.user_role"
	GROUP_ROLE = "platform.group_role"
	ROLE_PERMISSION = "platform.role_permission"


__all__ = ["Resource", "ResourcePermissionAction"]
