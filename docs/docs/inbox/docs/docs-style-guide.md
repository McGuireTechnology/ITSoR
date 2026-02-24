# Docs Style Guide

This guide defines authoring standards for ITSoR documentation.

## Scope

Use this page as the canonical standard for:

- Tone and voice
- Heading structure
- Code block language tags
- Command formatting

## Tone and Voice

- Write in clear, direct, task-oriented language.
- Prefer active voice and imperative phrasing for procedural steps.
- Keep statements specific and verifiable.
- Avoid marketing language and subjective claims.

Examples:

- Preferred: `Run backend migrations before starting the API service.`
- Avoid: `You should probably run migrations first to be safe.`

## Heading Standards

- Use one H1 (`#`) per page.
- Use H2 (`##`) for major sections.
- Use H3 (`###`) only when needed to split a major section.
- Keep headings short and action-oriented.

Preferred section naming:

- `Guide` for step-by-step procedural docs.
- `Reference` for factual definitions and parameter catalogs.
- `How-to` for narrow, task-specific outcomes.
- `Runbook` for incident/operations response workflows.

## Code Block Language Tags

Always include a language tag on fenced blocks.

- Use `bash` for POSIX or cross-shell command snippets.
- Use `powershell` only for Windows-specific command variants.
- Use `dotenv` for environment variable files.
- Use `yaml` for workflow/config examples.
- Use `text` for non-executable plain output.

Examples:

```bash
make backend-dev
```

```powershell
Copy-Item .env.example .env
```

## Command Formatting Standards

- Prefer `make` targets when they exist.
- Provide direct command alternatives only when needed for clarity or platform fallback.
- Use one command per line unless chaining is required.
- Keep paths relative to repository root when possible.
- Use consistent executable style (`python -m ...`) for cross-platform Python commands.

## Cross-Platform Command Rules

- If a command differs by OS, provide both variants with clear labels.
- Do not label generic commands as `powershell`.
- Document Windows no-`make` fallback only where setup requires it.

## Author Checklist

Before opening a docs PR, confirm:

- Heading hierarchy is valid and minimal.
- Code fences include correct language tags.
- Commands are copy/paste-ready.
- Links resolve to canonical pages.
- Content does not duplicate an existing canonical source.

## Related Internal Docs

- [Contributing](contributing.md)
- [Information Architecture](information-architecture.md)
- [Getting Started](getting-started.md)
- [Documentation Cleanup TODO](todo/documentation-cleanup.md)
