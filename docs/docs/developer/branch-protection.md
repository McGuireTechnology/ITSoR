# Branch Protection Guidance

This project should protect the `main` branch with required reviews and required checks.

## Recommended `main` branch rules

In GitHub repository settings, configure branch protection for `main` with:

- Require a pull request before merging
- Require approvals: at least 1
- Dismiss stale approvals when new commits are pushed
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Do not allow force pushes
- Do not allow deletions

## Required checks

Require CI checks from the umbrella workflow (`CI`) to pass before merge:

- docs checks
- backend checks
- frontend checks
- web checks

Use the exact check names shown in your repository after recent workflow runs.

## Optional hardening

- Require conversation resolution before merge
- Restrict who can push to matching branches
- Enable signed commits for `main`
- Require linear history

## Admin policy

Use "Do not allow bypassing the above settings" unless emergency break-glass is required by your org policy.

If break-glass is allowed, document who can use it and require post-incident review.
