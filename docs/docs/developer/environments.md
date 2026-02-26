# Environment Naming and Promotion Flow

This project uses three deployment environments:

- `dev`
- `stage`
- `prod`

## Environment purpose

### `dev`

- Fast feedback for active development.
- Receives changes from merges to `main`.
- May include unfinished or recently integrated features.

### `stage`

- Pre-production validation environment.
- Mirrors production configuration as closely as practical.
- Used for release candidate verification and stakeholder review.

### `prod`

- Live customer-facing environment.
- Receives only approved and validated releases.

## Naming conventions

Use these names consistently across tooling:

- CI/CD environments: `dev`, `stage`, `prod`
- Secrets/variables scopes: `DEV_*`, `STAGE_*`, `PROD_*`
- Deployment labels/tags: `env/dev`, `env/stage`, `env/prod`

## Promotion flow

1. **Develop and merge to `main`**
   - CI must pass (docs, backend, frontend, web checks).
2. **Deploy to `dev` automatically**
   - Triggered by successful `main` pipeline.
3. **Promote `dev` artifact to `stage`**
   - Use the same build artifact; do not rebuild from different sources.
   - Run smoke and integration checks in `stage`.
4. **Approve promotion to `prod`**
   - Require manual approval and change summary.
5. **Deploy to `prod`**
   - Promote the already-validated `stage` artifact.
6. **Post-deploy verification**
   - Run health checks and rollback if SLO/SLA thresholds fail.

## Promotion rules

- Promote artifacts forward (`dev` → `stage` → `prod`) without rebuilding.
- Require at least one human approval before `prod` promotion.
- Block `prod` if `stage` checks fail.
- Keep deployment logs and release notes for each promotion.

## Release cadence guidance

- `dev`: continuous
- `stage`: on release-candidate demand (often daily/weekly)
- `prod`: planned release windows with rollback readiness

## Related implementation docs

- [Backend Deployment and Runtime Guide](backend-deployment-runtime.md)
- [Backend Environment Variable Reference](backend-env.md)
