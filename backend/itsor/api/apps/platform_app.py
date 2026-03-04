from fastapi import FastAPI

from itsor.api.routes.groups import router as groups_router
from itsor.api.routes.platform_group_memberships import router as group_memberships_router
from itsor.api.routes.platform_rbac import router as platform_rbac_router
from itsor.api.routes.tenants import router as tenants_router
from itsor.api.routes.users import router as users_router

app = FastAPI(
    title="ITSoR Platform API",
    description="Platform sub-application for users, tenants, groups, and RBAC resources",
    version="0.1.0",
)

app.include_router(users_router)
app.include_router(tenants_router)
app.include_router(groups_router)
app.include_router(group_memberships_router)
app.include_router(platform_rbac_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
