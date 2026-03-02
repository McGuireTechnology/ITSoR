# Platform Domain Models

# Essential objects for platform management
# Role Based Access Control (RBAC) Support


from dataclasses import dataclass, field
from itsor.domain.ids import generate_ulid
from itsor.domain.models.base_model import BaseModel

# Core


# User (Global)
@dataclass
class PlatformUser:
    id: str = field(default_factory=generate_ulid)
    username: str = ""
    email: str = ""
    password_hash: str = ""

# Tenant
@dataclass
class PlatformTenant:
    id: str = field(default_factory=generate_ulid)
    name: str = ""

# Group (Scoped to Tenant)  
@dataclass
class PlatformGroup:
    id: str = field(default_factory=generate_ulid)
    name: str = ""
    tenant_id: str | None = None

# Role (Scoped to Tenant)
@dataclass
class PlatformRole:
    id: str = field(default_factory=generate_ulid)
    name: str = ""
    tenant_id: str | None = None
    description: str = ""

# Permission (Global)
@dataclass
class PlatformPermission:
    """
    Invariant:
        (resource, action, effect) must be unique across all permissions.
    """
    id: str = field(default_factory=generate_ulid)
    name: str = ""
    resource: str = ""
    action: str = ""
    effect: str = "allow"


# Junctions

# Every junction must enforce uniqueness at the DB layer:

# User-Tenant Junction
@dataclass
class PlatformUserTenant:
    id: str = field(default_factory=generate_ulid)
    user_id: str = ""
    tenant_id: str = ""

# Group-User Junction (Tenant Implied by Group)
@dataclass
class PlatformGroupMembership:
    id: str = field(default_factory=generate_ulid)
    group_id: str = ""
    user_id: str = ""

# User-Role Junction
@dataclass
class PlatformUserRole:
    id: str = field(default_factory=generate_ulid)
    user_id: str = ""
    role_id: str = ""

# Group-Role Junction (Tenant Implied by Group)
@dataclass
class PlatformGroupRole:
    id: str = field(default_factory=generate_ulid)
    group_id: str = ""
    role_id: str = ""

# Role-Permission Junction (Tenant Implied by Role)
@dataclass
class PlatformRolePermission:
    id: str = field(default_factory=generate_ulid)
    role_id: str = ""
    permission_id: str = ""





