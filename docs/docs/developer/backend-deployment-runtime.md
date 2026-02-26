# Backend Deployment and Runtime Guide

This guide defines backend runtime expectations for service process model, persistence, migrations, and rollback operations.

## Scope

This page covers:

- Service process model
- Persistence model and runtime dependencies
- Migration workflow and deployment sequencing
- Rollback strategy and incident handling

## Service Process Model

Backend runtime is a single FastAPI application process served by Uvicorn.

Local development command:

```bash
make backend-dev
```

Production process expectations:

1. Run as a managed long-lived service (systemd, container orchestrator, or equivalent process supervisor).
2. Expose a stable bind host/port behind a reverse proxy or ingress.
3. Ensure process restart policy is enabled for crash recovery.
4. Keep runtime logs centralized and timestamped.

Health check endpoint:

- `GET /health`

Subapp health checks:

- `GET /grc/health`
- `GET /itam/health`
- `GET /cmdb/health`

## Persistence Model

Primary persistence uses SQLAlchemy with backend DB URL from `BACKEND_DATABASE_URL`.

Current default (local):

- `sqlite:///./backend/itsor.db`

Production persistence requirements:

1. Use a managed relational database (not local SQLite files).
2. Configure secure credentials and network boundaries.
3. Ensure routine backup policy exists for primary database.
4. Validate restore path before production release windows.

Related runtime variables are documented in:

- [Backend Environment Variable Reference](backend-env.md)

### PostgreSQL production profile

Use a PostgreSQL-backed `BACKEND_DATABASE_URL` in production:

```dotenv
BACKEND_DATABASE_URL=postgresql+psycopg://itsor_app:<strong-password>@db.internal.example:5432/itsor
```

Profile checklist:

1. Provision PostgreSQL database and least-privilege app user.
2. Store DB credentials in secret manager (never committed in repo).
3. Set `BACKEND_DATABASE_URL` in deployment environment.
4. Validate network access between backend runtime and PostgreSQL.
5. Run migrations before traffic cutover.

## Migration Workflow

Schema changes are managed through Alembic migrations.

Standard migration command:

```bash
make backend-migrate
```

Direct command equivalent:

```bash
python -m alembic -c backend/alembic.ini upgrade head
```

Deployment sequencing for schema-affecting releases:

1. Deploy application artifact to target environment.
2. Run migrations against target database.
3. Verify service and health checks.
4. Verify key auth and critical API paths.

### PostgreSQL migration path

When moving from local SQLite workflows to PostgreSQL production:

1. Set production `BACKEND_DATABASE_URL` to PostgreSQL URL.
2. Run Alembic migrations against PostgreSQL target:

```bash
python -m alembic -c backend/alembic.ini upgrade head
```

1. Verify schema objects and indexes are present.
2. Run post-migration smoke checks (`/health`, `/auth/token`, `/auth/me`).

Migration safety rules:

- Prefer additive migrations first, destructive cleanup later.
- Avoid irreversible changes in the same step as application rollout when possible.
- Keep migration scripts idempotent within Alembic revision semantics.

## Rollback Strategy

Rollback includes both application and schema posture.

### Application rollback

1. Re-deploy prior known-good backend artifact.
2. Re-run service health checks.
3. Validate critical auth/API flows.

### Schema rollback

Use Alembic downgrade only when the target revision is validated as safe.

```bash
python -m alembic -c backend/alembic.ini downgrade -1
```

For high-risk migrations, prefer restore-based recovery:

1. Stop write traffic.
2. Restore from tested database backup/snapshot.
3. Re-deploy known-good application version.
4. Re-validate service and API health.

## Release Checklist (Backend Runtime)

- Runtime env vars validated (`BACKEND_ENV`, `BACKEND_DATABASE_URL`, auth/cookie settings).
- Database backup/snapshot freshness confirmed.
- Migration plan reviewed for backward compatibility.
- Rollback path and owner confirmed before deploy.
- Post-deploy health checks green.

## Related Internal Docs

- [Environments](environments.md)
- [Backend Environment Variable Reference](backend-env.md)
- [Backend Auth Setup Guide](backend-auth-setup.md)
- [Architecture](architecture.md)

## Next steps

- Validate API contract impact for backend changes: [API Reference Strategy](api-reference-strategy.md)
- Continue with contribution workflow and checks: [Developer Guide](index.md)
