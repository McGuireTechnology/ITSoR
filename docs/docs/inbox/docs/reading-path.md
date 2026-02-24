# Reading Path

Use this path to move from platform intent to implementation details with minimal context switching.

## Canonical sequence

1. [System Definition](system-definition.md)
   - Establishes what ITSoR is, what it is not, and core domain constraints.
2. [Architecture](architecture.md)
   - Maps repository structure, boundaries, and backend subapp route context.
3. [Domain Model Reference](domain-model-reference.md)
   - Defines asset entities, relationships, control assertions, evidence, and drift snapshot structure.
4. [Standards Baseline](standards-baseline.md)
   - Defines governance/control standards and data-model requirements.
5. [References](references.md)
   - Provides external source material backing architecture and control choices.
6. Subapp/API docs
   - [API Reference Strategy](api-reference-strategy.md)
   - [Backend Deployment and Runtime Guide](backend-deployment-runtime.md)
   - [Security Runbooks](security-runbooks.md)
   - [Backend Auth Setup](backend-auth-setup.md)
   - [Frontend Auth Integration](frontend-auth-integration.md)
   - [Developer Guide](developer/README.md)

## When to use this path

- New contributors learning why platform decisions exist.
- Reviewers validating traceability from design intent to implementation.
- Engineers preparing to add new backend/frontend capabilities.
