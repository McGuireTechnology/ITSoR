# ADR-0002: Backend Slice Package Layout Standard

- **Status:** Accepted
- **Date:** 2026-02-20
- **Owners:** Backend
- **Applies to:** `grc`, `itam`, `cmdb`, `custom`, `idam`, and future backend slices

## Context

The backend is moving to domain-oriented slices, but directory naming and placement are currently inconsistent across modules. We need one canonical package layout so use-case code, ports, adapters, routes, and schemas are predictable and discoverable.

## Decision

For each backend slice, standardize on this package layout:

- `backend/app/{slice}/api/routes/{entity}.py`
- `backend/app/{slice}/api/schemas/{entity}.py`
- `backend/app/{slice}/api/deps/{entity}.py`
- `backend/app/{slice}/domain/models/{entity}.py` (or `domain/models.py`)
- `backend/app/{slice}/domain/use_cases/{entity}.py`
- `backend/app/{slice}/domain/ports/{entity}.py`
- `backend/app/{slice}/infrastructure/container/container.py`
- `backend/app/{slice}/infrastructure/adapters/{adapter}.py`
- `backend/app/{slice}/infrastructure/models/{entity}.py` (when persistence/integration models are needed)

Where:

- `{slice}` is a domain slice (`grc`, `itam`, `cmdb`, `custom`, `idam`, etc.).
- `{entity}` is a bounded domain concept (for example `asset`, `control`, `policy`, `evidence`).

The layout uses three separate model types:

- **Domain model**: core business entities/value objects in `domain/models/{entity}.py`.
- **API schema model**: request/response contracts in `api/schemas/{entity}.py`.
- **Infrastructure model**: persistence/integration-facing representations in `infrastructure/models/{entity}.py` and/or adapter-specific mapper structures.

## Rules

1. `api/routes` define FastAPI handlers and map HTTP concerns to domain use cases.
2. `api/deps` holds request-scoped dependency providers.
3. `infrastructure/container/container.py` is the slice composition root and owns wiring of infrastructure adapters to domain use cases.
4. `domain/use_cases` orchestrate application flow and depend on `domain/ports` abstractions.
5. `domain/ports` define contracts used by use cases (repository/external service interfaces).
6. `infrastructure/*` implements external system and translation concerns (adapters, persistence, and composition wiring); infrastructure models do not leak into domain models.
7. `domain/models` define domain models only and remain framework-agnostic.
8. `api/schemas` define API I/O and validation contracts for route boundaries.

## Consequences

### Positive

- Consistent module discovery for contributors and code review.
- Clear dependency boundaries aligned with hexagonal architecture.
- Easier incremental migration from centralized `models.py`/`schemas.py` to slice-local modules.

### Trade-offs

- More files and directories per slice, especially during early feature development.
- Requires team discipline to avoid bypassing ports/use-case boundaries.

## Migration Guidance

- New backend work should use this structure by default.
- Existing modules can migrate incrementally without a full rewrite.
- Shared or legacy code may temporarily remain in common modules until slice-local replacements are complete.

### Current Adoption

- `grc`, `itam`, `cmdb`, `custom`, and `idam` use the `api/domain/infrastructure` layered package roots.
- Compatibility wrappers may remain at slice root modules during migration to preserve stable imports.
