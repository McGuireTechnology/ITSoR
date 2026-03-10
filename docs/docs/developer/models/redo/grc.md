# Governance Risk Compliance Domain Models

GRC models provide policy-to-evidence traceability and risk-informed decision support across all ITSoR slices.

## Scope

- Governance policy hierarchy and control catalogs
- Risk identification, scoring, treatment, and exception lifecycle
- Control assertions, evidence linkage, and assessment outcomes
- Compliance obligations and attestation history

## Core Entities

| Entity | Purpose | Required Fields |
| --- | --- | --- |
| `policy_document` | Authoritative policy/standard/procedure artifact | `policy_id`, `policy_type`, `title`, `owner_principal_id`, `version`, `state`, `effective_from`, `effective_to` |
| `control_objective` | Outcome-oriented objective linked to frameworks | `objective_id`, `name`, `description`, `criticality`, `state` |
| `control_requirement` | Atomic requirement mapped to framework control IDs | `control_id`, `framework_id`, `requirement_text`, `control_family`, `state` |
| `control_assertion` | Expected state bound to specific targets | `assertion_id`, `control_id`, `target_type`, `target_id`, `evaluation_method`, `frequency`, `severity`, `state` |
| `evidence_record` | Immutable evidence reference and normalized observation | `evidence_id`, `assertion_id`, `observed_at`, `collector_id`, `source_system`, `raw_ref`, `result_status` |
| `risk_register_entry` | Canonical risk item | `risk_id`, `title`, `category`, `likelihood`, `impact`, `inherent_score`, `residual_score`, `owner_principal_id`, `state` |
| `risk_treatment_plan` | Mitigation/transfer/acceptance plan | `treatment_id`, `risk_id`, `strategy`, `due_at`, `status`, `success_criteria` |
| `exception_record` | Time-bounded approved exception | `exception_id`, `control_id`, `target_id`, `justification`, `approved_by`, `expires_at`, `state` |

## Relationships

- `policy_document` `defines` `control_objective`
- `control_objective` `decomposes_to` `control_requirement`
- `control_requirement` `is_asserted_by` `control_assertion`
- `control_assertion` `is_evidenced_by` `evidence_record`
- `control_assertion` `informs` `risk_register_entry`
- `risk_register_entry` `is_addressed_by` `risk_treatment_plan`
- `exception_record` `temporarily_overrides` `control_assertion`

## Lifecycle States

### `risk_register_entry.state`

- `identified`
- `analyzed`
- `treated`
- `accepted`
- `closed`

### `control_assertion.state`

- `draft`
- `active`
- `suspended`
- `retired`

### `exception_record.state`

- `requested`
- `approved`
- `expired`
- `revoked`

## Scoring Model Expectations

- Inherent score is computed before controls.
- Residual score is computed after current control effectiveness.
- Score methodology is versioned (formula + thresholds) and tied to evaluation timestamps.
- Changes to risk appetite or scoring criteria create a new scoring-method version.

## Standards Alignment

| Standard | Mapping |
| --- | --- |
| ITIL v4 | Governance, Risk Management, Information Security Management, Continual Improvement |
| CIS Controls v8 | Controls 1-18 as measurable safeguard requirements and evidence targets |
| NIST CSF 2.0 | `GV` (Govern), `ID` (Identify), `PR` (Protect), `DE` (Detect), `RS` (Respond), `RC` (Recover) functions |
| NIST SP 800-53 Rev. 5 | Control baselines for requirement and assertion libraries |
| ISO/IEC 27001:2022 | ISMS policy, risk treatment, control implementation, and internal audit traceability |
| COBIT 2019 | Governance objectives and enterprise control management alignment |

## Cross-Slice Dependencies

- Control targets resolve to Platform, IDM, and ITAM entities.
- Evidence sources include auth/session events and asset telemetry.
- Risk owners resolve to IDM principals and Platform users.
