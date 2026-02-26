# Contributing to ITSoR

Thanks for contributing.

The canonical contribution process, standards, and release expectations are maintained in:

- [docs/contributing.md](docs/contributing.md)

Please read that guide before opening a pull request.

## Frontend API client sync gate

CI verifies that generated frontend API artifacts match the backend OpenAPI contract.

If CI fails on generated client drift, run from repository root:

```bash
make frontend-api-client
```

Then commit updated files under:

- `frontend/openapi/schema.json`
- `frontend/src/api/generated/`

## Quick links

- Project overview: [README.md](README.md)
- Security reporting: [SECURITY.md](SECURITY.md)
- Docs site: https://docs.itsor.app
