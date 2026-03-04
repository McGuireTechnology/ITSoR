import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from itsor.api.apps.idm_app import app as idm_app
from itsor.api.apps.platform_app import app as platform_app
from itsor.api.routes.auth import router as auth_router
from itsor.api.routes.entity_records import router as entity_records_router
from itsor.api.routes.entity_types import router as entity_types_router
from itsor.api.routes.namespaces import router as namespaces_router
from itsor.api.routes.workspaces import router as workspaces_router
from itsor.infrastructure.database.sqlalchemy import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


def _get_cors_origins() -> list[str]:
    configured = os.getenv("CORS_ALLOW_ORIGINS", "").strip()
    if configured:
        return [origin.strip() for origin in configured.split(",") if origin.strip()]

    host = os.getenv("HOST", "127.0.0.1")
    frontend_port = os.getenv("FRONTEND_PORT", "5173")
    fallback_origins = {
        f"http://{host}:{frontend_port}",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    }
    return sorted(fallback_origins)


def _get_cors_origin_regex() -> str:
    return os.getenv(
        "CORS_ALLOW_ORIGIN_REGEX",
        r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    )


app = FastAPI(
    title="ITSoR API",
    description="IT System of Record API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_cors_origins(),
    allow_origin_regex=_get_cors_origin_regex(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(workspaces_router)
app.include_router(namespaces_router)
app.include_router(entity_types_router)
app.include_router(entity_records_router)
app.mount("/platform", platform_app)
app.mount("/idm", idm_app)


@app.api_route("/users", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def redirect_users_root():
    return RedirectResponse(url="/platform/users", status_code=307)


@app.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def redirect_users_path(path: str):
    return RedirectResponse(url=f"/platform/users/{path}", status_code=307)


@app.api_route("/tenants", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def redirect_tenants_root():
    return RedirectResponse(url="/platform/tenants", status_code=307)


@app.api_route("/tenants/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def redirect_tenants_path(path: str):
    return RedirectResponse(url=f"/platform/tenants/{path}", status_code=307)


@app.api_route("/groups", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def redirect_groups_root():
    return RedirectResponse(url="/platform/groups", status_code=307)


@app.api_route("/groups/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def redirect_groups_path(path: str):
    return RedirectResponse(url=f"/platform/groups/{path}", status_code=307)


@app.get("/")
def read_root():
    return {"message": "ITSoR API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
