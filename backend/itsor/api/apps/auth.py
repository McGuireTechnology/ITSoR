from fastapi import FastAPI

from itsor.api.routes.auth import (
    group_membership_router,
    group_role_router,
    group_router,
    permission_router,
    role_permission_router,
    role_router,
    tenant_router,
    user_role_router,
    user_router,
    user_tenant_router,
)

app = FastAPI(
    title="ITSoR : Auth API",
    description="Authentication and Authorization sub-application",
    version="0.1.0",
)

app.include_router(user_router)
app.include_router(group_router)
app.include_router(tenant_router)
app.include_router(role_router)
app.include_router(permission_router)
app.include_router(user_tenant_router)
app.include_router(group_membership_router)
app.include_router(user_role_router)
app.include_router(group_role_router)
app.include_router(role_permission_router)
