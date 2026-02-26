# System Definition

## Positioning

ITSoR is not a CMDB clone. It is an asset-centric, control-aware operational knowledge platform.

Internal framing:

- **State-backed control intelligence platform**

The platform combines:

- Asset inventory
- Configuration state and drift tracking
- Identity and dependency relationships
- Control expectation mapping
- Evidence-backed control evaluation
- Historical posture reconstruction

## Core Architectural Decisions

- **Primary anchor:** asset
- **Primary storage model:** relational database
- **Relationships:** first-class entities
- **Versioning:** full historical versioning of state/assertions
- **Control reconstruction:** historical reconstruction is required

These decisions are required for defensible drift and posture analysis over time.

## Domain Layers

### 1) Asset Layer (what exists)

Minimum first-class asset categories:

- Hardware assets
- Virtual assets
- Software instances (deployed instances, not product catalog only)
- Human and service identities
- Data assets/classifications
- Network constructs
- Documentation/policy artifacts
- Contracts/licenses

### 2) Control Layer (what should be true)

Controls attach to concrete operational entities (assets/services/identities/data), not only to org-level abstractions.

### 3) Evidence Layer (what is provably true)

Evidence is linked to control assertions and observed state so the platform can answer:

- Which assets violate which controls?
- Which control assertions lack current evidence?
- What was compliant/non-compliant at a specific historical time?

### 4) Drift Layer (how state changes)

Drift requires temporal state discipline:

- Baseline/expected state definitions
- Periodic or event-driven snapshots/assertions
- State deltas and violation windows
- Alerts prioritized by criticality/exposure

## Data Modeling Rules

- Avoid a single polymorphic “CI blob” model.
- Avoid storing critical operational state as unbounded JSON without normalized assertions.
- Never overwrite authoritative state in-place when historical reconstruction is required.
- Model relationships explicitly with validity windows.

## Standards Alignment

Primary alignment references:

- ISO/IEC 19770 (ITAM)
- CIS Controls / NIST SP 800-53 / ISO 27001 mappings
- OSCAL as interchange/transport
- SPDX/CPE for software/platform inventory facets
- CVE/CVSS/OVAL/SCAP for vulnerability/evidence integrations

Standards are reference/interoperability layers, not a replacement for the domain model.

## North-Star Capability

A useful output should be deterministic and queryable:

- Asset state over time
- Control assertion over time
- Evidence linkage over time
- Drift timeline over time
- Posture impact from failures and exposure paths

If these chains cannot be reconstructed, posture claims are not reliable.

## Next steps

- Translate intent into implementation structure: [Architecture](architecture.md)
- Review canonical entity and relationship structure: [Domain Model Reference](domain-model-reference.md)
- Trace standards and control model requirements: [Standards Baseline](standards-baseline.md)
- Follow the full sequence: [Reading Path](reading-path.md)
