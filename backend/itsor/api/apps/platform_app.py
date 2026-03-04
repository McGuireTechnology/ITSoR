from fastapi import FastAPI

from itsor.api.routes.platform_routes import router as platform_routes_router

app = FastAPI(
    title="ITSoR Platform API",
    description="Platform sub-application for users, tenants, groups, and RBAC resources",
    version="0.1.0",
)

app.include_router(platform_routes_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
