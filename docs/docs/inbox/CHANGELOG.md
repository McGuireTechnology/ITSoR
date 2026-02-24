# Changelog

All notable changes to this project are documented in this file.

## 2026-02-18 - Baseline Setup

### Added

- Initial platform scaffold for docs, backend, frontend, and web applications.
- MkDocs Material configuration, docs navigation, and operational documentation.
- FastAPI backend foundation with tests, lint/format tooling, and integration tests.
- Vue + Vite frontend and web apps with lint/test scripts and CI build checks.
- Repository governance and hygiene baseline:
  - CODEOWNERS
  - PR and issue templates
  - SECURITY.md and CODE_OF_CONDUCT.md
  - root CONTRIBUTING.md
  - pre-commit hooks
  - Dependabot automation
  - GitHub Actions hardening (least privilege permissions, concurrency, SHA-pinned actions, CodeQL)

### Commits

- cd8ace0 - feat(platform): scaffold docs, backend, and Vue apps
- bddb997 - chore(repo): add governance, CI hardening, and security policy
