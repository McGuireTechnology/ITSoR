from fastapi import FastAPI

from itsor.api.routes.idm_group_memberships_routes import router as group_memberships_router
from itsor.api.routes.idm_groups_routes import router as groups_router
from itsor.api.routes.idm_identities_routes import router as identities_router
from itsor.api.routes.idm_people_routes import router as people_router
from itsor.api.routes.idm_users_routes import router as users_router

app = FastAPI(
    title="ITSoR IDM API",
    description="Identity Data Management sub-application",
    version="0.1.0",
)

app.include_router(people_router)
app.include_router(identities_router)
app.include_router(users_router)
app.include_router(groups_router)
app.include_router(group_memberships_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
