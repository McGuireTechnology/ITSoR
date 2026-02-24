# Security Runbooks

This page defines operational runbooks for security-sensitive auth events.

## Scope

This runbook set covers:

- Auth incidents
- Secret rotation
- Emergency token invalidation

## Runbook 1: Auth Incident Response

Use this runbook when suspicious login/session behavior is detected (credential stuffing, session hijack suspicion, abnormal token activity).

### Triggers

- Repeated failed logins across many accounts
- Unexpected successful logins from unusual sources
- Sudden spike in `401`/`403` after auth changes
- Reports of users being logged out or impersonation suspicion

### Immediate actions (first 15 minutes)

1. Declare incident and assign incident owner.
2. Freeze auth-related deployments and config changes.
3. Capture current environment/auth settings snapshot.
4. Confirm backend auth endpoints are reachable and healthy.
5. Start incident timeline with UTC timestamps.

### Containment actions

1. Force logout/high-risk account invalidation where feasible.
2. Restrict suspicious source ranges at edge/proxy controls.
3. Increase auth event logging detail for active investigation.
4. Require password reset for suspected affected accounts.

### Verification checklist

- `POST /auth/token` behavior matches expected controls.
- `GET /auth/me` returns only valid session identity.
- No unauthorized privilege escalation is observed.
- Incident timeline includes all mitigation actions.

## Runbook 2: JWT Secret Rotation

Use this runbook for scheduled key hygiene or immediate response after secret exposure suspicion.

### Pre-rotation checks

1. Generate new strong secret in approved secret manager.
2. Confirm deployment path for backend environment variables.
3. Prepare user communication for expected forced re-auth.
4. Schedule rotation window and rollback owner.

### Rotation steps

1. Update `JWT_SECRET` in target environment.
2. Restart/redeploy backend service to load new secret.
3. Validate auth endpoints and login flow.
4. Confirm new token issuance works.

### Post-rotation behavior

- Existing tokens signed with the old secret become invalid.
- Users may need to authenticate again.

### Rollback (if needed)

1. Restore previous secret value in environment.
2. Restart backend service.
3. Re-validate auth flows and incident status.

## Runbook 3: Emergency Token Invalidation

Use this runbook when immediate session/token invalidation is required.

### Emergency triggers

- Confirmed secret compromise
- Confirmed active token abuse
- Critical auth logic regression in production

### Invalidation strategy

Primary immediate control:

1. Rotate `JWT_SECRET` to invalidate all active JWTs.

Additional controls:

1. Invalidate active session cookies via app logout policy and re-auth enforcement.
2. Temporarily restrict sensitive routes if abuse is active.

### Execution checklist

1. Announce emergency change to responders.
2. Rotate secret and redeploy backend.
3. Verify old tokens fail and new tokens succeed.
4. Confirm critical endpoints return expected auth statuses.
5. Communicate user impact and re-login requirement.

## Incident Artifacts Checklist

For each incident/rotation event, retain:

- UTC timeline of actions
- Who executed each action
- Config values changed (without exposing secrets in plain text)
- Validation outputs (health and auth endpoint checks)
- Final incident summary and follow-up actions

## Related Internal Docs

- [Backend Auth Setup Guide](backend-auth-setup.md)
- [Backend Environment Variable Reference](backend-env.md)
- [Auth Token Expiry and Refresh Strategy](auth-token-strategy.md)
- [Backend Deployment and Runtime Guide](backend-deployment-runtime.md)

## Next steps

- Review auth token lifecycle and rotation behavior: [Auth Token Expiry and Refresh Strategy](auth-token-strategy.md)
- Return to implementation and troubleshooting paths: [User Guide](user/README.md)
