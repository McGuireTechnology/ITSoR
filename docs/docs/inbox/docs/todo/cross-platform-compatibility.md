# Cross-Platform Compatibility TODO

Priority legend: `P1` = current sprint critical, `P2` = near-term, `P3` = follow-on.

Owner legend: `Backend`, `Frontend`, `Docs`, `DevOps`, `Security`.

## Scan Summary (2026-02-19)

Initial Windows/macOS compatibility scan identified shell and path assumptions that can block local setup.

### Completed in this pass

- [x] [P1][Owner: DevOps] Make root `makefile` virtualenv/tool paths cross-platform (`.venv/Scripts` vs `.venv/bin`) and remove Windows-only hardcoded executable paths.
- [x] [P1][Owner: Docs] Replace Windows-only docs build command in getting started with `make docs-build`.
- [x] [P1][Owner: Docs] Replace Windows-only direct backend auth commands with cross-platform `python -m ...` guidance.

### Remaining follow-up items

- [ ] [P2][Owner: DevOps] Add a small cross-platform sanity script/target that validates expected tool entry points (`python`, `pip`, `mkdocs`, `uvicorn`, `alembic`, `ruff`) after `make venv`.
- [ ] [P2][Owner: Docs] Add explicit OS-specific quickstart variants (Windows PowerShell vs macOS/Linux shell) in `docs/getting-started.md`.
- [ ] [P3][Owner: DevOps] Evaluate replacing `cd <dir> && npm ...` in `makefile` with `npm --prefix <dir> ...` for cleaner shell behavior across environments.
- [x] [P1][Owner: Docs] Normalize command fence labeling in onboarding docs (`powershell` currently used for mixed shell examples) to reduce copy/paste errors on macOS.
- [x] [P1][Owner: DevOps] Add a CI smoke job that runs `make venv && make docs-install && make backend-install` on both `windows-latest` and `macos-latest`.
- [x] [P1][Owner: Docs] Document Windows prerequisite path for `make` (or provide no-`make` command equivalents) in `README.md` and `docs/getting-started.md`.
- [x] [P1][Owner: DevOps] Make `make venv` resilient on Windows where `python` launcher is unavailable by adding a `py -3`/`python3` fallback strategy.

## Additional Findings (Repo-wide scan, 2026-02-19)

- `README.md` and `docs/getting-started.md` currently require `make` but do not provide a Windows-native fallback path when GNU Make is not installed.
- `makefile` target `venv` currently shells out to `python -m venv .venv`; some Windows environments expose only `py` by default.
- GitHub Actions workflows currently run only on `ubuntu-latest`; cross-platform behavior is inferred rather than continuously validated.

## Notes

- Scan focus: root `makefile`, onboarding docs, and backend docs command snippets.
- Current changes were limited to high-impact setup blockers and docs accuracy updates.
