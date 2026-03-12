# OSCAL Assessment Layer: Assessment Results Model

## Purpose

The OSCAL Assessment Results model defines the information contained within an assessment report supporting assessment and continuous monitoring capabilities.

## Authors and Consumers

### Assessment Results Authors

- Assessors
- Continuous assessment tools

Assessors develop assessment results to report what was assessed, how it was assessed, who performed the assessment, what was found, and what risks were identified.

### Assessment Results Consumers

- System owners
- Authorizing officials
- Continuous assessment monitoring practitioners

System owners consume assessment results to understand system risk posture, target risks for remediation, and plan remediation activities. Authorizing officials use assessment results in adjudication activities related to authorization decisions. Continuous assessment monitoring practitioners use the results to monitor ongoing security posture.

## Assessment Results Organization

An OSCAL Assessment Results document is organized as follows:

- **Metadata**: Required in all OSCAL models. Includes title, version, publication and modification timestamps, OSCAL version, roles, parties, and locations.
- **Import AP**: Identifies the OSCAL Assessment Plan (AP) used for this assessment and links the assessed system context (including the SSP).
- **Local Definitions**: Defines activities or control objectives not present in the linked AP/SSP.
- **Results**: Captures findings, identified risks, recommended remediation, and related adjudication details (for example, false positives, risk adjustments, operationally required risks, and expiration timing).
- **Reviewed Controls**: Identifies controls actually reviewed by the assessment.
- **Assessment Subjects**: Identifies in-scope system elements (for example, locations, components, inventory items, users).
- **Assessment Assets**: Identifies assessor assets used during assessment (team, tools, and rules of engagement context).
- **Attestation**: Captures assessor assertions.
- **Assessment Log**: Tracks performed actions with start/end timestamps and optional links to assessment activities.
- **Observations**: Captures individual observations and related evidence.
- **Risks**: Captures individual risks including weakness descriptions, risk statements, and characteristics.
- **Findings**: Captures findings derived from observations and risks, including control objective status where applicable.
- **Back Matter**: Standard OSCAL back matter for attachments, citations, and embedded resources.

## Key Concepts

The Assessment Results model is part of the OSCAL Assessment Layer and provides machine-readable XML, JSON, and YAML representations for assessment reporting.

This model is typically used by assessors and continuous monitoring practitioners to communicate the degree to which a system complies with one or more frameworks.

It supports both point-in-time assessments and continuous assessment reporting, including scope, activity timing, observations, findings, and identified risks.

Assessment Results are always defined in the context of an OSCAL Assessment Plan (AP). Through the AP linkage, results are associated with the assessed system.

The current model evolved from FedRAMP Security Assessment Report information requirements and expanded to support continuous assessment use cases.

The model intentionally aligns syntax with:

- the Assessment Plan model (for objectives, subjects, assets, and activities), and
- the POA&M model (for results and risk expression).

## Important Note to Developers

Each time OSCAL file content changes, update both of the following:

1. Assign a new UUID to the root element's `uuid`.
2. Update `metadata.last-modified` to the save timestamp.

These mechanisms allow tools to quickly detect document changes. The document-level UUID is the OSCAL UUID associated with version control semantics.

When converting between formats (for example, XML to JSON), these values should remain the same so tools can recognize equivalent content across representations.
