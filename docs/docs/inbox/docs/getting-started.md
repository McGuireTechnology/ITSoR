# Getting Started

This is the **canonical onboarding and quickstart source** for ITSoR.

## 0) Clone the repository

```bash
git clone <your-repo-url>
cd ITSoR
```

## Prerequisites

- Python 3.13+
- Node.js 20+
- `make`

### Windows note (`make`)

If GNU Make is not installed on Windows, either install it (for example `choco install make`) or use the no-`make` command equivalents below.

## 1) Create environment and install dependencies

```bash
make venv
make docs-install
make backend-install
make frontend-install
make web-install
```

Optional all-in-one install:

```bash
make install
```

### No-`make` equivalents (Windows PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -r requirements/docs.txt
.\.venv\Scripts\python.exe -m pip install -r requirements/backend.txt
cd frontend
npm install
cd ..
cd web
npm install
cd ..
```

## 2) Configure host and ports (optional)

```bash
cp .env.example .env
```

On Windows PowerShell, use:

```powershell
Copy-Item .env.example .env
```

Defaults:

- Docs: `127.0.0.1:3003`
- Backend: `127.0.0.1:3002`
- Frontend: `127.0.0.1:3000`
- Web: `127.0.0.1:3001`

## 3) Run local services

Run each service in a separate terminal.

### Documentation site

```bash
make docs-dev
```

Open: <http://127.0.0.1:3003>

### Backend API

```bash
make backend-dev
```

Open: <http://127.0.0.1:3002>

### Frontend app

```bash
make frontend-dev
```

Open: <http://127.0.0.1:3000>

### Web app

```bash
make web-dev
```

Open: <http://127.0.0.1:3001>

## 4) Build static docs

```bash
make docs-build
```

Output is generated in the `site/` directory.

## 5) Daily developer workflow

```bash
git pull
make venv
make frontend-install
```

Run core checks before opening a PR:

```bash
pytest backend/tests -q
cd frontend
npm run lint
npm run test
```

## Next steps

- Move from setup to system context: [System Definition](system-definition.md)
- Continue through implementation structure: [Reading Path](reading-path.md)
- Find docs by content type and audience: [Information Architecture](information-architecture.md)
