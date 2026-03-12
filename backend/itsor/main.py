import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from itsor.api.apps import auth_app, itam_app, oscal_app
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
    docs_url=None,
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
app.mount("/itam", itam_app)
app.mount("/oscal", oscal_app)


class ActiveAppEntry(BaseModel):
    key: str
    title: str
    mount_path: str
    docs_url: str | None = None
    openapi_url: str | None = None


class ActiveAppsResponse(BaseModel):
    apps: list[ActiveAppEntry]


def _join_mounted_path(mount_path: str, sub_path: str | None) -> str | None:
    if not sub_path:
        return None

    normalized_mount = mount_path.rstrip("/") or "/"
    normalized_sub = sub_path if sub_path.startswith("/") else f"/{sub_path}"
    return f"{normalized_mount}{normalized_sub}"


def _active_apps() -> list[ActiveAppEntry]:
    mounted_apps = [
        ("auth", "/auth", auth_app),
        ("itam", "/itam", itam_app),
        ("oscal", "/oscal", oscal_app),
    ]

    return [
        ActiveAppEntry(
            key=key,
            title=sub_app.title,
            mount_path=mount_path,
            docs_url=_join_mounted_path(mount_path, sub_app.docs_url or "/docs"),
            openapi_url=_join_mounted_path(mount_path, sub_app.openapi_url or "/openapi.json"),
        )
        for key, mount_path, sub_app in mounted_apps
    ]


@app.get("/")
def read_root():
    return {"message": "ITSoR API is running"}


@app.get("/apps", response_model=ActiveAppsResponse)
def list_active_apps() -> ActiveAppsResponse:
    return ActiveAppsResponse(apps=_active_apps())


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui() -> HTMLResponse:
    apps_with_docs = [item for item in _active_apps() if item.docs_url]
    utility_links = "".join(
        [
            '<a href="/docs">Root API</a>',
        ]
    )
    menu_links = "".join(
        f'<a href="{item.docs_url}">{item.title}</a>'
        for item in apps_with_docs
    )
    fixed_menu_html = f"""
<nav class=\"itsor-swagger-app-menu-fixed\" aria-label=\"Application docs\">
    <strong>Apps</strong>
    {utility_links}
    {menu_links}
</nav>
"""

    swagger = get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=f"{app.title} - Swagger UI",
    )

    body_bytes = bytes(swagger.body)
    body = body_bytes.decode("utf-8")
    injection = """
<style>
    .itsor-swagger-app-menu-fixed {
        position: sticky;
        top: 0;
        z-index: 100001;
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        background: #1f2937;
        color: #ffffff;
        font-family: sans-serif;
        font-size: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.18);
    }
    .itsor-swagger-app-menu-fixed a {
        color: #ffffff;
        text-decoration: none;
        border: 1px solid rgba(255, 255, 255, 0.35);
        border-radius: 4px;
        padding: 2px 8px;
        line-height: 1.4;
    }
    .itsor-swagger-app-menu-fixed a:hover,
    .itsor-swagger-app-menu-fixed a:focus-visible {
        background: rgba(255, 255, 255, 0.14);
        text-decoration: none;
    }
    .swagger-ui .topbar {
        display: flex;
        align-items: center;
        gap: 10px;
        padding-right: 12px;
    }
    .swagger-ui .topbar .itsor-app-docs-links {
        margin-left: auto;
    }
    .itsor-app-docs-links {
        display: inline-flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px;
        font-family: sans-serif;
        font-size: 12px;
        color: #ffffff;
    }
    .itsor-app-docs-links strong {
        font-weight: 600;
        opacity: 0.92;
    }
    .itsor-app-docs-links a {
        color: #ffffff;
        text-decoration: none;
        border: 1px solid rgba(255, 255, 255, 0.35);
        border-radius: 4px;
        padding: 2px 8px;
        line-height: 1.4;
    }
    .itsor-app-docs-links a:hover,
    .itsor-app-docs-links a:focus-visible {
        background: rgba(255, 255, 255, 0.14);
        text-decoration: none;
    }
</style>
<script>
    (function attachAppLinksToSwaggerTopbar() {
        let hasInjected = false;

        const addLinks = async () => {
            if (hasInjected) {
                return;
            }

            const topbar = document.querySelector('.swagger-ui .topbar');
            if (!topbar) {
                return;
            }

            if (topbar.querySelector('.itsor-app-docs-links')) {
                hasInjected = true;
                return;
            }

            const appsEndpoint = new URL('./apps', window.location.href).toString();
            const response = await fetch(appsEndpoint, { credentials: 'include' }).catch(() => null);
            if (!response || !response.ok) {
                return;
            }

            const payload = await response.json().catch(() => ({}));
            const apps = Array.isArray(payload && payload.apps) ? payload.apps : [];
            const appsWithDocs = apps.filter((item) => item && item.docs_url);
            if (!appsWithDocs.length) {
                return;
            }

            const nav = document.createElement('nav');
            nav.className = 'itsor-app-docs-links';
            nav.setAttribute('aria-label', 'Application docs links');

            const label = document.createElement('strong');
            label.textContent = 'Apps';
            nav.appendChild(label);

            const rootApiLink = document.createElement('a');
            rootApiLink.href = '/docs';
            rootApiLink.textContent = 'Root API';
            nav.appendChild(rootApiLink);

            for (const appEntry of appsWithDocs) {
                const link = document.createElement('a');
                link.href = appEntry.docs_url;
                link.textContent = appEntry.title || appEntry.key || appEntry.docs_url;
                nav.appendChild(link);
            }

            topbar.appendChild(nav);
            hasInjected = true;
        };

        const observer = new MutationObserver(() => {
            void addLinks();
        });

        const start = () => {
            void addLinks();
            window.setTimeout(() => void addLinks(), 250);
            window.setTimeout(() => void addLinks(), 1000);
            observer.observe(document.documentElement, { childList: true, subtree: true });
            window.setTimeout(() => observer.disconnect(), 8000);
        };

        if (document.readyState === 'loading') {
            window.addEventListener('DOMContentLoaded', start, { once: true });
        } else {
            start();
        }
    })();
</script>
"""
    body = body.replace("<body>", f"<body>{fixed_menu_html}", 1)
    body = body.replace("</body>", f"{injection}</body>")
    response_headers = dict(swagger.headers)
    response_headers.pop("content-length", None)
    return HTMLResponse(content=body, status_code=swagger.status_code, headers=response_headers)


@app.get("/health")
def health_check():
    return {"status": "ok"}
