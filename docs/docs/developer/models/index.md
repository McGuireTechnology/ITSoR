# Domain Models

This section defines the core domain slices for ITSoR.

## Modeling Intent

- `Index`, `Auth`, and `Platform` are operational slices that enable ITSoR to run.
- `GRC`, `IDM`, and `ITAM` are value slices that explain why ITSoR exists.
- All slices align to canonical identifiers, temporal history, and explicit relationships.

## Slices

- [Auth Domain Models](auth.md)
- [Platform Domain Models](platform.md)
- [Governance Risk Compliance Domain Models](grc.md)
- [Identity Management Domain Models](idm.md)
- [IT Asset Management Domain Models](itam.md)
- [DDI Domain Models](ddi.md)

## Roadmap

- [Domain Slice Roadmap](../todo/domain-slice-roadmap.md)

## Shared Modeling Rules

All slices should apply these rules:

1. Every first-class entity has an immutable internal ID.
2. State changes are auditable and reconstructable over time.
3. Cross-slice links use stable references, not embedded copies.
4. Assertions and evidence are linked for controls and risk.
5. Owner and steward identities resolve to IDM principals.
6. Cross-domain user/person association should use explicit mapping tables (not inline foreign keys).
7. Platform person display attributes should resolve through mappings to IDM current identity records.
