# ITSoR Branding Guide

This guide defines the baseline brand standards for ITSoR across docs and frontend surfaces.

## Brand Positioning

- Product name: **ITSoR**
- Expanded name: **IT System of Record**
- Primary tone: clear, operational, trustworthy
- Writing style: direct, technical, and outcome-focused

## Voice and Messaging

Use language that emphasizes control, clarity, and auditability.

Preferred themes:

- System reliability
- Operational confidence
- Traceable decisions
- Cross-functional alignment

Avoid:

- Vague marketing language
- Overstated claims (for example: “fully automated everything”)
- Inconsistent naming (`IT SoR`, `Itsor`, etc.)

## Naming Conventions

- Use `ITSoR` in titles and product references.
- Use `IT System of Record` on first mention in long-form docs when clarity helps.
- Keep domain labels consistent (`CMDB`, `ITAM`, `GRC`, `IDAM`, etc.).

## Color and Theme Direction

Current interface direction uses deep purple/indigo with pink accent in docs and a neutral professional base in app screens.

Guidelines:

- Use theme tokens/config where available.
- Prefer semantic usage (primary, accent, muted, danger) over hard-coded ad-hoc colors.
- Ensure contrast meets accessibility expectations for text and controls.

## Typography

- Primary UI/document font: `Inter` (docs theme)
- Code font: `JetBrains Mono` (docs theme)
- Keep heading hierarchy consistent (`H1` once, then `H2/H3` logically).

## Logo and Mark Usage

- Keep clear space around logos/marks.
- Do not stretch, skew, or recolor logos outside approved variants.
- Use high-contrast logo variants on dark backgrounds.

## UI Consistency Rules

- Reuse shared layout and component patterns.
- Keep spacing, corner radius, and control density consistent within a page.
- Use consistent labels for auth actions (`Signup`, `Login`, `Logout`).

## Documentation Branding Rules

- Keep docs navigation labels concise and action-oriented.
- Prefer canonical page names over duplicate alternatives.
- Keep examples copy/paste ready and environment-accurate.

## Accessibility Baseline

- Maintain visible focus states.
- Preserve keyboard navigation for primary flows.
- Avoid relying on color alone to convey status.

## Frontend Implementation Notes

The frontend currently supports both utility-first and component CSS workflows.

- Tailwind CSS can be used for rapid utility styling.
- Bootstrap can be used for standardized component primitives.
- When both are present, avoid class conflicts by favoring one approach per component.

## Governance

- Branding updates should be reviewed alongside UX and docs impact.
- Any major brand changes should include before/after screenshots in pull requests.
