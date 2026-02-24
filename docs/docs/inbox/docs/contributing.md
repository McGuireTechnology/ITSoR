# Contributing

## Docs contribution workflow

1. Create or update the relevant page in `docs/`
2. Run `mkdocs serve` and verify formatting and links
3. Keep headings concise and task-oriented
4. Open a pull request with a clear summary of changes

## Writing conventions

- Use imperative headings (`Install`, `Configure`, `Troubleshoot`)
- Prefer short steps with concrete commands
- Include examples for error-prone tasks
- Follow canonical docs standards: [Docs Style Guide](docs-style-guide.md)

## Quality checklist

- [ ] Navigation updated in `mkdocs.yml`
- [ ] Links and commands validated
- [ ] No duplicated guidance across pages

## Frontend API client sync gate

CI verifies that generated frontend API artifacts match the backend OpenAPI contract.

If CI fails on generated client drift, run from repository root:

```bash
make frontend-api-client
```

Then commit updated files under:

- `frontend/openapi/schema.json`
- `frontend/src/api/generated/`

## Pre-commit checks

Repository hooks are configured in `.pre-commit-config.yaml` and include lint checks for backend, docs, frontend, and web.

Install and enable hooks:

```bash
pre-commit install
```

Run all hooks manually:

```bash
pre-commit run --all-files
```

## Release process

1. Merge approved pull requests into `main`.
2. Confirm CI is green (docs, backend, frontend, and web workflows).
3. Prepare release summary from merged PRs.
4. Create a version tag and publish release notes.
5. Validate post-release deployment targets (docs and web).

## Tagging convention

Use lightweight or annotated git tags with one of these formats:

- `vMAJOR.MINOR.PATCH` for release versions (recommended)
- `baseline-YYYY-MM-DD` for non-release baseline snapshots

Examples:

- `v0.1.0`
- `v1.4.2`
- `baseline-2026-02-18`

### Tagging checklist

1. Ensure `main` is clean and CI is passing.
2. Confirm `CHANGELOG.md` includes release notes.
3. Create tag locally:

```bash
git tag v0.1.0
```

1. Push tag to origin:

```bash
git push origin v0.1.0
```

1. Create GitHub release notes referencing the same tag.

## Changelog expectations

Each pull request should include a short changelog-ready entry in its description:

- **Type**: `feature`, `fix`, `docs`, `chore`
- **Scope**: affected area (`backend`, `frontend`, `web`, `docs`, `infra`)
- **Summary**: one sentence describing impact
- **Breaking change**: `none` or clear migration action

Suggested format:

```text
Type: feature
Scope: backend
Summary: Added health endpoint for service readiness checks.
Breaking change: none
```
