# Audience Map

This page defines the canonical audience model for ITSoR documentation and assigns each top-level page to one primary audience.

## Audience Model

- `operator`: runs and monitors platform services day-to-day.
- `developer`: builds and changes backend/frontend/docs code.
- `security/reviewer`: assesses controls, risk posture, and evidence quality.
- `admin`: owns access, policy, and governance decisions.

## Top-Level Page Assignment

| Page | Primary Audience | Secondary Audience |
| --- | --- | --- |
| `README.md` (Home) | developer | operator |
| `getting-started.md` | developer | operator |
| `local-config.md` | developer | operator |
| `backend-env.md` | developer | operator |
| `backend-auth-setup.md` | developer | security/reviewer |
| `frontend-auth-integration.md` | developer | operator |
| `auth-token-strategy.md` | security/reviewer | developer |
| `standards-baseline.md` | security/reviewer | admin |
| `references.md` | developer | security/reviewer |
| `environments.md` | operator | admin |
| `branch-protection.md` | admin | developer |
| `deploy-docs.md` | operator | developer |
| `branding.md` | developer | admin |
| `developer/todo/index.md` | developer | admin |
| `developer/todo/documentation-and-operations.md` | docs | developer |
| `user/index.md` | operator | admin |
| `developer/index.md` | developer | operator |
| `architecture.md` | developer | security/reviewer |
| `system-definition.md` | admin | security/reviewer |
| `adr/README.md` | developer | admin |
| `contributing.md` | developer | admin |

## Alignment Rule

When creating or modifying top-level docs pages:

1. Assign exactly one primary audience.
2. Keep page scope and examples optimized for that primary audience.
3. Add cross-links for secondary audiences instead of mixing multiple guides into one page.