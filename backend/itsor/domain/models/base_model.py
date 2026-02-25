from dataclasses import dataclass, field
from enum import IntEnum

from itsor.domain.ids import generate_ulid


OWNER_PERMISSIONS_SHIFT = 6
GROUP_PERMISSIONS_SHIFT = 4
WORLD_PERMISSIONS_SHIFT = 2

PERMISSIONS_MASK = 0b11
OWNER_PERMISSIONS_MASK = 0b11000000
GROUP_PERMISSIONS_MASK = 0b00110000
WORLD_PERMISSIONS_MASK = 0b00001100
CONTROL_FLAGS_MASK = 0b00000011


class PermissionLevel(IntEnum):
    NONE = 0b00
    READ = 0b01
    WRITE = 0b10
    READ_WRITE = 0b11


class PermissionControlFlag(IntEnum):
    ACL_LOCKED = 0b01
    INHERIT_PERMISSIONS = 0b10


DEFAULT_OWNER_PERMISSIONS = PermissionLevel.READ_WRITE
DEFAULT_GROUP_PERMISSIONS = PermissionLevel.READ_WRITE
DEFAULT_WORLD_PERMISSIONS = PermissionLevel.NONE
DEFAULT_CONTROL_FLAGS = 0
DEFAULT_PERMISSIONS = (
    (int(DEFAULT_OWNER_PERMISSIONS) << OWNER_PERMISSIONS_SHIFT)
    | (int(DEFAULT_GROUP_PERMISSIONS) << GROUP_PERMISSIONS_SHIFT)
    | (int(DEFAULT_WORLD_PERMISSIONS) << WORLD_PERMISSIONS_SHIFT)
    | DEFAULT_CONTROL_FLAGS
)


def _set_bit_pair(source: int, value: int, shift: int) -> int:
    if not 0 <= value <= PERMISSIONS_MASK:
        raise ValueError("Permissions bit pair must be between 0 and 3")
    cleared = source & ~(PERMISSIONS_MASK << shift)
    return cleared | ((value & PERMISSIONS_MASK) << shift)


@dataclass
class BaseModel:
    name: str = ""
    owner_id: str | None = None
    group_id: str | None = None
    permissions: int = DEFAULT_PERMISSIONS
    id: str = field(default_factory=generate_ulid)

    def __post_init__(self) -> None:
        if not 0 <= self.permissions <= 0xFF:
            raise ValueError("permissions must be a single byte (0-255)")

    @property
    def owner_permissions(self) -> int:
        return (self.permissions & OWNER_PERMISSIONS_MASK) >> OWNER_PERMISSIONS_SHIFT

    @owner_permissions.setter
    def owner_permissions(self, value: int) -> None:
        self.permissions = _set_bit_pair(self.permissions, value, OWNER_PERMISSIONS_SHIFT)

    @property
    def group_permissions(self) -> int:
        return (self.permissions & GROUP_PERMISSIONS_MASK) >> GROUP_PERMISSIONS_SHIFT

    @group_permissions.setter
    def group_permissions(self, value: int) -> None:
        self.permissions = _set_bit_pair(self.permissions, value, GROUP_PERMISSIONS_SHIFT)

    @property
    def world_permissions(self) -> int:
        return (self.permissions & WORLD_PERMISSIONS_MASK) >> WORLD_PERMISSIONS_SHIFT

    @world_permissions.setter
    def world_permissions(self, value: int) -> None:
        self.permissions = _set_bit_pair(self.permissions, value, WORLD_PERMISSIONS_SHIFT)

    @property
    def control_flags(self) -> int:
        return self.permissions & CONTROL_FLAGS_MASK

    @control_flags.setter
    def control_flags(self, value: int) -> None:
        self.permissions = _set_bit_pair(self.permissions, value, 0)

    @property
    def inherits_permissions(self) -> bool:
        return bool(self.control_flags & PermissionControlFlag.INHERIT_PERMISSIONS)

    @inherits_permissions.setter
    def inherits_permissions(self, enabled: bool) -> None:
        flags = self.control_flags
        bit = int(PermissionControlFlag.INHERIT_PERMISSIONS)
        flags = (flags | bit) if enabled else (flags & ~bit)
        self.control_flags = flags

    @property
    def is_acl_locked(self) -> bool:
        return bool(self.control_flags & PermissionControlFlag.ACL_LOCKED)

    @is_acl_locked.setter
    def is_acl_locked(self, enabled: bool) -> None:
        flags = self.control_flags
        bit = int(PermissionControlFlag.ACL_LOCKED)
        flags = (flags | bit) if enabled else (flags & ~bit)
        self.control_flags = flags
