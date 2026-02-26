# Security Policy

## Reporting a Vulnerability

Please do **not** report security vulnerabilities through public GitHub issues.

Use one of these private channels instead:

1. GitHub Security Advisories (preferred):
   - https://github.com/nmcguire/ITSoR/security/advisories/new
2. Email the maintainers:
   - security@itsor.app

When reporting, include:

- Affected component (`backend`, `frontend`, `web`, `docs`, or workflow/config)
- Reproduction steps or proof of concept
- Impact assessment (what can an attacker do?)
- Suggested remediation (if known)

## Response Process

- **Acknowledgement target:** within 2 business days
- **Triage target:** within 5 business days
- **Fix timeline:** based on severity and exploitability
- **Disclosure:** coordinated disclosure after a fix is available or mitigations are documented

We may ask for additional details during triage and will keep report details confidential until coordinated disclosure.

## Supported Versions

Because ITSoR is currently under active development, only the latest `main` branch state is supported for security fixes.

## Security Best Practices for Contributors

- Never commit secrets, tokens, credentials, or private keys.
- Use `.env` files locally and keep them out of version control.
- Keep dependencies updated via Dependabot PRs.
- Prefer least-privilege permissions for CI workflows and cloud credentials.
