# ITSoR Documentation

Welcome to the **ITSoR** docs hub.

!!! info "Current public presence"
    The canonical documentation site is `https://docs.itsor.app` and is hosted on GitHub Pages.

## What this site includes

- Project setup and onboarding details
- Architecture and system context
- Contribution workflow and documentation standards

## Quick links

- Start here: [Getting Started](getting-started.md)
- Follow the concept-to-implementation flow: [Reading Path](reading-path.md)
- Learn the structure: [Architecture](architecture.md)
- Find canonical doc locations: [Information Architecture](information-architecture.md)
- Audience assignments: [Audience Map](audience-map.md)
- Contribute updates: [Contributing](contributing-guide.md)

## Role-based entry points

- Operator: [Getting Started](getting-started.md) -> [Environments](environments.md) -> [User Guide](../user/index.md)
- Developer: [Getting Started](getting-started.md) -> [Architecture](architecture.md) -> [Developer Guide](index.md)
- Security/Reviewer: [System Definition](system-definition.md) -> [Standards Baseline](standards-baseline.md) -> [References](references.md)
- Admin: [System Definition](system-definition.md) -> [Branch Protection](branch-protection.md) -> [Contributing](contributing-guide.md)

## Onboarding source of truth

Use [Getting Started](getting-started.md) as the canonical onboarding/quickstart source.
Avoid duplicating setup instructions in other docs pages.

## Documentation principles

!!! tip "Keep docs actionable"
    Prefer steps, examples, and checklists over abstract descriptions.

!!! note "Single source of truth"
    Use this site for canonical process and implementation guidance.
## Current features

### Documentation platform

- MkDocs Material site with custom dark blue/purple/hot pink branding
- Canonical docs URL configured for `https://docs.itsor.app`
- Structured navigation for getting started, architecture, guides, contributing, and project TODOs

### Application projects

- FastAPI backend scaffold with root and health endpoints
- Vue + Vite frontend scaffold for product application
- Vue + Vite web scaffold for the public marketing site

### Local developer workflow

- Root `makefile` for environment setup, dependency install, and dev servers
- Root `.env`-driven host and port configuration for all local services
- VS Code Tasks integrated with make targets for one-click execution

### Repository automation

- CI umbrella workflow with reusable jobs for docs, backend, frontend, and web checks
- Path-filtered workflow triggers to reduce unnecessary CI runs
- Dependabot automation for GitHub Actions, Python, and npm dependencies

### Standards and consistency

- `.editorconfig` and `.gitattributes` for formatting and line-ending consistency
- Unified dependency layout with umbrella `requirements.txt` and split docs/backend requirement files

## Next steps

- Follow onboarding: [Getting Started](getting-started.md)
- Use the guided sequence: [Reading Path](reading-path.md)
- Review doc ownership and canonical locations: [Information Architecture](information-architecture.md)
