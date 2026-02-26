# Documentation Information Architecture

This page defines where key documentation topics live so readers can find canonical guidance quickly and avoid overlap.

## Core content map

| Content type | Canonical location | Purpose |
| --- | --- | --- |
| Concept | [System Definition](system-definition.md) | Problem framing, product scope, and operating model. |
| Architecture | [Architecture](architecture.md) | Technical structure, boundaries, and implementation direction. |
| API | [API Reference Strategy](api-reference-strategy.md), [Backend Auth Setup](backend-auth-setup.md), and [Frontend Auth Integration](frontend-auth-integration.md) | Contract policy, integration behavior, and auth contract usage. |
| Operations | [Environments](environments.md), [Backend Env Vars](backend-env.md), [Branch Protection](branch-protection.md), [Docs Deployment](deploy-docs.md) | Runtime, configuration, governance, and deployment execution. |
| Backlog | [TODO Hub](todo/index.md) and [Documentation and Operations TODO](todo/documentation-and-operations.md) | Planned work, priorities, and ownership. |

## Audience-oriented entry points

- Operator/Admin: [Getting Started](getting-started.md) -> [Environments](environments.md) -> [Branch Protection](branch-protection.md)
- Developer: [Getting Started](getting-started.md) -> [Architecture](architecture.md) -> [Developer Guide](index.md)
- Security/Reviewer: [System Definition](system-definition.md) -> [Standards Baseline](standards-baseline.md) -> [References](references.md)

## Authoring guardrails

- Keep onboarding in [Getting Started](getting-started.md) as the source of truth.
- Avoid duplicating setup/runbook details outside their canonical page.
- Add new pages to this map when introducing new top-level domains.
