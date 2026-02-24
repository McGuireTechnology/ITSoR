# Standards Baseline for ITSoR

This page defines the standards baseline for an ITSoR platform spanning:

- CMDB
- ITAM
- GRC
- Security controls and compliance reporting

## Recommended standards stack

Use a layered standards approach.

### Service and configuration model (CMDB)

- ITIL 4 practices for service and configuration management
- Service model patterns aligned to CSDM-style concepts:
  - business application
  - business service
  - technical service
  - service offering
  - configuration item relationships and dependencies

### Asset governance (ITAM)

Use the ISO/IEC 19770 family:

- ISO/IEC 19770-1: ITAM management system requirements
- ISO/IEC 19770-2: software identification tags (SWID)
- ISO/IEC 19770-3: entitlement schema
- ISO/IEC 19770-5: overview and vocabulary

### Security outcomes and control operations

- CIS Controls v8 as the actionable control set
- NIST CSF 2.0 as outcome and governance structure:
  - Govern
  - Identify
  - Protect
  - Detect
  - Respond
  - Recover

### Compliance data exchange and automation

- OSCAL as the machine-readable format for controls, implementations, assessments, and POA&M

## Platform data model requirements

### CMDB core

- CI classes and attributes
- ownership and support model
- environment and lifecycle state
- service dependency graph
- criticality and data classification

### ITAM core

- hardware and software asset records
- contracts, vendors, and procurement linkage
- entitlement and license position
- install/use evidence
- EOL and EOS tracking

### GRC core

- canonical control catalog
- control implementation statements
- evidence objects and attestations
- test procedures and test results
- findings, issues, and exceptions
- risk register and treatment plans

### OSCAL artifacts to support

- `catalog` and `profile`
- `component-definition`
- `system-security-plan` (SSP)
- `assessment-plan` (SAP)
- `assessment-results` (SAR)
- `plan-of-action-and-milestones` (POA&M)

## Control mapping strategy

Adopt one internal canonical control ID per control objective.

For each control, maintain mappings to:

- CIS Controls v8 safeguard IDs
- NIST CSF 2.0 categories/subcategories
- (optional) NIST SP 800-53 Rev. 5 control IDs

This allows one implementation and one evidence set to satisfy multiple reporting views.

## Implementation phases

### Phase 1: Foundational model

- Stand up CMDB and ITAM minimum schema
- Establish canonical control catalog
- Build CIS v8 to NIST CSF 2.0 mapping table

### Phase 2: Operational GRC workflows

- Add evidence collection workflow
- Add control testing workflow
- Add findings, risk, and exception handling

### Phase 3: Compliance automation

- Implement OSCAL import/export pipeline
- Produce machine-generated SSP/SAR/POA&M views
- Add dashboarding for control posture and audit readiness

## Governance guidance

- Define data ownership for each domain (CMDB, ITAM, GRC)
- Set evidence freshness SLAs by control criticality
- Require exception expiry and periodic recertification
- Version control baselines and control mappings

## Next steps

- Review source frameworks and tool references: [References](references.md)
- Map standards intent to backend API and auth integration: [Backend Auth Setup](backend-auth-setup.md)
- Continue with client-side integration behavior: [Frontend Auth Integration](frontend-auth-integration.md)
