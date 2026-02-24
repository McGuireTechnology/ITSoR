# Developer Guide

!!! warning "MkDocs 2.0 + Material for MkDocs"
    Material for MkDocs currently warns about MkDocs 2.0 compatibility and recommends planning migration to Zensical.
    Current ITSoR docs are pinned to a compatible MkDocs 1.x + Material 9.x setup and continue to build successfully.

## Purpose

This guide is for engineers contributing to ITSoR services, frontend, and documentation.

## Local Development

### Prerequisites

- Complete canonical onboarding first: [Getting Started](../getting-started.md).
- Use this guide for contributor workflow and local quality checks after initial setup.

### Environment and runtime setup

Canonical setup and service startup are documented in [Getting Started](../getting-started.md):

- Environment creation and dependency installation
- Optional `.env` creation and local host/port defaults
- Docs/backend/frontend/web local run commands

For backend runtime variable behavior and CORS details, see:

- [Backend Environment Variable Reference](../backend-env.md)
- [Local Host and Port Configuration](../local-config.md)

### Optional re-bootstrap commands

If you need to refresh your local environment after onboarding:

```bash
make venv
make install
```

### Service startup

See [Getting Started](../getting-started.md#3-run-local-services) for canonical startup commands.

### Optional local host/port template creation

macOS/Linux shell:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

## Local quality checks

### Backend lint/format/tests

```bash
make backend-lint
pytest backend/tests -q
```

### Frontend and web lint/tests

```bash
cd frontend
npm run lint
npm run test

cd ../web
npm run lint
npm run test
```

### Pre-commit hooks

```bash
pre-commit install
pre-commit run --all-files
```

## Repository Layout

- `docs/` Documentation source for MkDocs
- `backend/` FastAPI application
- `frontend/` Vue + Vite product UI
- `web/` Vue + Vite marketing site
- `tests/` cross-project integration/e2e scaffolding
- `.github/workflows/` CI and deployment workflows

## Contribution Workflow

1. Create a feature branch.
2. Make focused changes.
3. Run local checks/builds and pre-commit hooks.
4. Open a pull request with context and testing notes.
