# ToDo / FixMe

## Core Scaffold Improvements

### P0 - Make Backend Runnable

- [ ] Add an application entrypoint in `backend/itsor/main.py` with:
	- [ ] app factory
	- [ ] health route
	- [ ] router registration
	- [ ] startup/shutdown hooks
- [ ] Implement dependency wiring in `backend/itsor/core/infrastructure/container/`.
- [ ] Expose container dependencies via `backend/itsor/core/api/deps/`.

### P0 - First End-to-End Domain Vertical

- [ ] Add first domain slice (example: asset or configuration item):
	- [ ] domain model in `backend/itsor/core/domain/models/`
	- [ ] port interface in `backend/itsor/core/domain/ports/`
	- [ ] use case in `backend/itsor/core/domain/use_cases/`
	- [ ] API route in `backend/itsor/core/api/routes/`
	- [ ] request/response schemas in `backend/itsor/core/api/schemas/`

### P1 - Persistence and Migrations

- [ ] Add persistence baseline in infrastructure:
	- [ ] SQLAlchemy models/repositories in `backend/itsor/core/infrastructure/repos/`
	- [ ] adapter implementations in `backend/itsor/core/infrastructure/adapters/`
- [ ] Initialize Alembic migration flow under `backend/alembic/`.
- [ ] Create first migration for the initial domain vertical.

### P1 - Configuration and Runtime Baseline

- [ ] Add shared settings/config module under `backend/itsor/common/`.
- [ ] Populate `backend/requirements.txt` with required runtime dependencies.
- [ ] Implement `backend/itsor/wsgi.py` if WSGI deployment is required.

### P2 - Test Foundation

- [ ] Add minimal test suite in `backend/tests/`:
	- [ ] API smoke test
	- [ ] domain use case unit test
	- [ ] repository contract test

### Notes

- Current structure is a strong clean-architecture scaffold (`api`, `domain`, `infrastructure`) and should be preserved.
- Focus on one complete vertical slice first before expanding module breadth.

