# API Reference Strategy

This page defines how ITSoR publishes and consumes backend API contracts.

## Scope

- Contract source: FastAPI-generated OpenAPI document from the backend service.
- Contract consumers: frontend and web clients, tests, and integration tooling.
- Policy owner: Backend (contract), with Frontend/QA consumers.

## OpenAPI Contract

The backend contract is generated from the running FastAPI app.

- OpenAPI JSON endpoint: `GET /openapi.json`
- Interactive docs endpoint: `GET /docs`
- Contract metadata source: `backend/app/main.py` (`title`, `version`, route tags, schemas)

### Contract publication rules

1. Treat OpenAPI output as the canonical API contract.
2. Every externally consumed route must include stable request/response models.
3. Group endpoints using route tags (`auth`, `grc`, `itam`, `cmdb`) to keep client generation predictable.
4. Prefer additive schema changes; avoid breaking field removals/renames without a version bump policy decision.

### Local contract snapshot workflow

Use this workflow when validating API changes in pull requests:

1. Start backend locally (`make backend-dev`).
2. Export a snapshot:

   ```bash
   curl -s http://127.0.0.1:3002/openapi.json > backend/openapi.snapshot.json
   ```

3. Compare snapshot diffs in PR review for contract-impacting changes.

## Generated Client Workflow

Current state:

- Frontend auth calls are currently hand-authored in `frontend/src/auth/client.js`.
- Generated clients are planned as the default for broader API coverage.

Target workflow:

1. Backend PR changes OpenAPI-producing code (routes, schemas, dependencies).
2. Export updated OpenAPI snapshot.
3. Regenerate typed client(s) from the snapshot.
4. Update frontend/web integration code to consume regenerated types/operations.
5. Validate with backend + frontend tests before merge.

### Implementation guidance

- Keep generated output in a dedicated client directory (for example `frontend/src/api/generated/`).
- Keep thin, hand-written wrappers for app-specific concerns (auth state, retries, UI errors).
- Do not edit generated files manually; regenerate from contract changes.

## Versioning Policy

API versioning follows semantic intent at the contract level.

### Change classification

- Patch-level (non-breaking): documentation updates, optional response additions, internal behavior fixes.
- Minor-level (backward-compatible): additive endpoints, additive optional request fields.
- Major-level (breaking): required field changes, type/shape incompatibility, endpoint removals/renames.

### Versioning rules

1. Reflect contract version in FastAPI app metadata (`version` in `backend/app/main.py`).
2. Document breaking changes in `CHANGELOG.md` with migration guidance.
3. For breaking changes, keep old/new behavior coexistence where practical during transition windows.
4. If parallel versions are introduced, expose explicit versioned route namespaces and sunset dates.

## Pull Request Checklist (API Changes)

- OpenAPI snapshot updated (or explicitly marked no contract change).
- Client generation step executed for impacted consumers.
- Backward-compatibility impact assessed and labeled.
- Versioning/changelog updates included when required.

## Related Internal Docs

- [Backend Auth Setup](backend-auth-setup.md)
- [Frontend Auth Integration](frontend-auth-integration.md)
- [Architecture](architecture.md)
- [References](references.md)

## Next steps

- Continue implementation details: [Developer Guide](index.md)
- Review governance alignment: [Standards Baseline](standards-baseline.md)
- Return to canonical sequence: [Reading Path](reading-path.md)