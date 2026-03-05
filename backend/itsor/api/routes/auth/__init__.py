from .group import router as group_router
from .group_membership import router as group_membership_router
from .group_role import router as group_role_router
from .permission import router as permission_router
from .role import router as role_router
from .role_permission import router as role_permission_router
from .tenant import router as tenant_router
from .user import router as user_router
from .user_role import router as user_role_router
from .user_tenant import router as user_tenant_router

__all__ = ["user_router", "group_router", "tenant_router", "role_router", "permission_router",
           "user_tenant_router", "group_membership_router", "user_role_router",
           "group_role_router", "role_permission_router"]
