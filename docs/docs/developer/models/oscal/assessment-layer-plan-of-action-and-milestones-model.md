# OSCAL Assessment Layer: Plan of Action and Milestones Model

## Purpose

The OSCAL Plan of Action and Milestones (POA&M) model defines the information contained within a POA&M.

## Authors and Consumers

### POA&M Authors

- Information System Security Officers (ISSOs)

ISSOs use a POA&M to identify risks to the system and track remediation activities on behalf of the system owner.

### POA&M Consumers

- System owners
- Authorizing officials
- Continuous monitoring practitioners
- Customers

System owners use the POA&M to understand risk posture and ensure remediation activities occur as planned. Authorizing officials use POA&M data for authorization adjudication and periodic review. Continuous monitoring practitioners use it to monitor system security posture over time.

## POA&M Organization

An OSCAL POA&M is organized as follows:

- **Metadata**: Required in all OSCAL models; includes title, version, publication and modification timestamps, OSCAL version, roles, parties, and locations.
- **Import SSP**: Identifies the OSCAL SSP for the assessed system, allowing POA&M content to reference system information instead of duplicating it.
- **System Identifier**: Supports uniquely identifying a system when a POA&M is delivered without an SSP.
- **Local Definitions**: Supports local component and inventory definitions when referenced items are not in the associated SSP.
- **Risk**: Captures individual risks, including weakness descriptions, risk statements, characteristics, and deviation/disposition details.
- **POA&M Items**: Enumerates each POA&M item with risk context, remediation plan, tracking, and status.
- **Back Matter**: Standard OSCAL back matter for attachments, citations, and embedded resources.

## Key Concepts

The OSCAL POA&M model is part of the OSCAL Assessment Layer and defines machine-readable XML, JSON, and YAML representations of POA&M information.

This model is used by roles responsible for tracking and reporting compliance issues or identified risks, typically on behalf of a system owner.

The model supports common POA&M needs, including discovery source, risk and recommendation details, remediation planning/tracking, and disposition status. It also supports deviations, such as false positive determinations, risk acceptance, and risk adjustments.

A POA&M is always scoped to a specific system. It must either be associated with an OSCAL SSP or reference a system using a unique system identifier.

The current model was derived from FedRAMP POA&M information requirements.

POA&M syntax aligns with Assessment Results for overlapping assemblies (especially observations and risks), enabling straightforward transfer of identified risks from assessment reporting to POA&M tracking.

## Important Note to Developers

Each time OSCAL file content changes, update both of the following:

1. Assign a new UUID to the root element's `uuid`.
2. Update `metadata.last-modified` to the save timestamp.

These mechanisms allow tools to quickly detect document changes. The document-level UUID is the OSCAL UUID associated with version control semantics.

When converting between formats (for example, XML to JSON), these values should remain the same so tools can recognize equivalent content across representations.
