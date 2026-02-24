# Architecture

## Repository layout

- `Apple/` platform-specific components
- `backend/` service and API implementation
- `frontend/` UI and client application code
- `docs/` this documentation site

## Documentation map

Use this section to keep architecture decisions discoverable:

1. System context
2. Service boundaries
3. Data flows
4. Deployment topology

Core architecture framing:

- [System Definition](system-definition.md)

## Decision records

Add Architecture Decision Records (ADRs) in a dedicated section when introducing major technical changes.

- ADR index: [Architecture Decision Records (ADRs)](adr/README.md)
- Latest: [ADR-0002: Backend Slice Package Layout Standard](adr/0002-backend-slice-package-layout.md)

## Backend subapp route map

The backend is mounted under `api.itsor.app` and uses root path prefixes (no `/api` prefix in route paths).

- `GET /grc/health`
- `GET /itam/health`
- `GET /cmdb/health`

These routes are registered from dedicated router modules in `backend/app/routers/` and included during backend app startup.

## Next steps

- Review canonical domain entities and temporal model rules: [Domain Model Reference](domain-model-reference.md)
- Align architecture decisions to controls and governance constraints: [Standards Baseline](standards-baseline.md)
- Review external standards and tooling context: [References](references.md)
- Continue to implementation-oriented docs: [Backend Auth Setup](backend-auth-setup.md)
