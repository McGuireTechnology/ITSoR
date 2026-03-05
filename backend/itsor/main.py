import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from itsor.api.apps import auth_app


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
app.mount("/auth", auth_app)
#app.mount("/platform", platform_app)
#app.mount("/idm", idm_app)
#app.mount("/custom", custom_app)

@app.get("/")
def read_root():
    return {"message": "ITSoR API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
