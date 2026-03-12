from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from itsor.api.routes.auth import (
    group_membership_router,
    group_role_router,
    group_router,
    navigation_router,
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
    docs_url=None,
)

app.include_router(group_router)
app.include_router(group_membership_router)
app.include_router(group_role_router)
app.include_router(navigation_router)
app.include_router(permission_router)
app.include_router(role_router)
app.include_router(role_permission_router)
app.include_router(tenant_router)
app.include_router(user_router)
app.include_router(user_role_router)
app.include_router(user_tenant_router)


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui() -> HTMLResponse:
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
    .itsor-swagger-app-menu-fixed a,
    .itsor-app-docs-links a {
        color: #ffffff;
        text-decoration: none;
        border: 1px solid rgba(255, 255, 255, 0.35);
        border-radius: 4px;
        padding: 2px 8px;
        line-height: 1.4;
    }
    .itsor-swagger-app-menu-fixed a:hover,
    .itsor-swagger-app-menu-fixed a:focus-visible,
    .itsor-app-docs-links a:hover,
    .itsor-app-docs-links a:focus-visible {
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
        color: #ffffff;
        font-family: sans-serif;
        font-size: 12px;
    }
</style>
<script>
    (function attachAppLinksToSwaggerTopbar() {
        let hasInjected = false;

        const addLinks = async () => {
            if (hasInjected) return;
            const topbar = document.querySelector('.swagger-ui .topbar');
            if (!topbar) return;
            if (topbar.querySelector('.itsor-app-docs-links')) {
                hasInjected = true;
                return;
            }

            const response = await fetch('/apps', { credentials: 'include' }).catch(() => null);
            if (!response || !response.ok) return;

            const payload = await response.json().catch(() => ({}));
            const apps = Array.isArray(payload && payload.apps) ? payload.apps : [];
            const appsWithDocs = apps.filter((item) => item && item.docs_url);

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
    fixed_menu_html = """
<nav class=\"itsor-swagger-app-menu-fixed\" aria-label=\"Application docs\">
    <strong>Apps</strong>
    <a href=\"/docs\">Root API</a>
    <a href=\"/auth/docs\">ITSoR : Auth API</a>
    <a href=\"/itam/docs\">ITSoR : ITAM API</a>
    <a href=\"/oscal/docs\">ITSoR : OSCAL API</a>
</nav>
"""
    body = body.replace("<body>", f"<body>{fixed_menu_html}", 1)
    body = body.replace("</body>", f"{injection}</body>")

    response_headers = dict(swagger.headers)
    response_headers.pop("content-length", None)
    return HTMLResponse(content=body, status_code=swagger.status_code, headers=response_headers)

