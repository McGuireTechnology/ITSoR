# ADR-0001: Hexagonal Ports/Adapters Boundaries for Vertical Slices

- **Status:** Accepted
- **Date:** 2026-02-19
- **Owners:** Backend
- **Related slices:** `grc`, `itam`, `cmdb`

## Context

The backend is moving toward vertical slices and needs explicit dependency boundaries so business logic remains testable and independent from framework and infrastructure details.

We now have a target package layout per slice:

- `backend/app/grc/{models,use_cases,ports,adapters,repos,routes,schemas,deps}`
- `backend/app/itam/{models,use_cases,ports,adapters,repos,routes,schemas,deps}`
- `backend/app/cmdb/{models,use_cases,ports,adapters,repos,routes,schemas,deps}`

Without explicit rules, framework code can leak into domain/application layers and increase coupling.

## Decision

Each slice follows a hexagonal architecture with these boundaries and rules:

1. **`domain` layer**
   - Contains entities, value objects, domain services, and pure business rules.
   - Must not import FastAPI, SQLAlchemy, HTTP clients, or adapter modules.

2. **`application` layer**
   - Contains use cases and port contracts (interfaces/protocols).
   - Defines inbound ports (how controllers/routers call use cases).
   - Defines outbound ports (repository/external service contracts required by use cases).
   - May depend on `domain`, but not on concrete adapter implementations.

3. **`adapters` layer**
   - Contains concrete implementations of outbound ports and framework bindings.
   - Includes persistence adapters, API clients, and web adapters.
   - Depends on `application` and `domain` as needed.

4. **Dependency direction**
   - Allowed: `adapters -> application -> domain`
   - Disallowed: `domain -> application|adapters`, `application -> adapters`

## Consequences

### Positive

- Improves testability by isolating business logic.
- Reduces framework lock-in by isolating FastAPI/ORM concerns in adapters.
- Enables incremental migration from existing route-level persistence logic to use-case orchestration.

### Trade-offs

- Adds up-front structure and more files per feature.
- Requires team discipline and CI/import-boundary checks to prevent regressions.

## Implementation Notes

- New backend features should start in slice packages (`grc`, `itam`, `cmdb`) and follow this dependency model.
- Existing endpoints can be migrated incrementally by introducing application use cases and moving persistence access behind outbound ports.
- A future CI rule should validate import boundaries automatically.
