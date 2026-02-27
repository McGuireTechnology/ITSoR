from fastapi import FastAPI

from itsor.api.routes.groups import router as groups_router
from itsor.api.routes.platform_endpoint_permissions import router as platform_endpoint_permissions_router
from itsor.api.routes.tenants import router as tenants_router
from itsor.api.routes.users import router as users_router

app = FastAPI(
    title="ITSoR Platform API",
    description="Platform sub-application for users, tenants, groups, and endpoint permissions",
    version="0.1.0",
)

app.include_router(users_router)
app.include_router(tenants_router)
app.include_router(groups_router)
app.include_router(platform_endpoint_permissions_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
