# Layers and Models

OSCAL architecture is organized as a stack of layers. Each lower layer defines information structures that are referenced by higher layers. Each layer contains one or more models, and each model serves a specific operational purpose while building on model content from lower layers.

## OSCAL Layer Stack

From top to bottom, OSCAL layers are:

- **Assessment Layer**
- **Implementation Layer**
- **Control Layer**

From dependency order (bottom to top), implementation relies on control content, and assessment relies on implementation and control content.

## Models by Layer

### Assessment Layer

- Assessment Plan model
- Assessment Results model
- Plan of Action and Milestones (POA&M) model

### Implementation Layer

- System Security Plan (SSP) model
- Component Definition model

### Control Layer

- Catalog model
- Profile model
- Control Mapping model

## Machine-Readable Formats

Each OSCAL model is represented in machine-readable formats such as:

- XML
- JSON
- YAML

These serializations provide encoding and exchange mechanisms for OSCAL content.

## Control Layer Overview

Cybersecurity frameworks define controls to reduce risk, often grouped into catalogs. Organizations then select applicable controls as a baseline (or overlay), potentially using multiple catalogs.

The Control layer provides:

- **Catalog model** for defining and organizing controls in a standard machine-readable format.
- **Profile model** for selecting, organizing, and tailoring a baseline of controls.
- **Control Mapping model** for describing relationships among controls and control elements across authoritative sources.

### Catalog Model

The catalog model is foundational for OSCAL. Controls used by other OSCAL artifacts are expected to originate in catalog content.

Catalog controls may include:

- requirement statements,
- parameters,
- references,
- objectives,
- assessment methods,
- and organizational structure/grouping.

### Profile Model

A profile imports controls from catalogs (or from other profiles that ultimately derive from catalogs), then enables control tailoring.

Tailoring can include:

- additions,
- changes,
- removals of statements,
- parameter adjustments,
- objective and assessment-action modifications.

Profiles enable transparency and traceability from tailored baselines back to original catalog definitions, while supporting automated baseline authoring.

### Control Mapping Model

The mapping model links source and target frameworks, standards, or baselines.

Each source control can map to one, many, or no target controls. Mapping relationships can include metadata such as:

- `equivalent-to`,
- `subset-of`,
- `intersects-with`,
- `no-relationship`,
- plus references and supporting notes.

This supports control coverage analysis and reduces duplicate effort across multiple frameworks.

## Implementation Layer Overview

The Implementation layer focuses on how a specific system implements a selected baseline and how reusable components contribute to that implementation.

A component can include policy, process, artifact evidence, hardware, software, or services.

### System Security Plan (SSP) Model

The SSP model expresses system security implementation in the context of a specific baseline/profile.

Machine-readable SSPs support:

- tool-based import,
- automated validation and authorization workflows,
- and transformation into human-readable documentation.

### Component Definition Model

The Component Definition model expresses details about individual components, including security-relevant configuration and how the component supports controls in a baseline.

SSP tools can import component definitions to pre-populate SSP content, then tailor details to match the actual deployed system.

## Assessment Layer Overview

The Assessment layer captures assessment planning, execution outcomes, supporting evidence, findings, and remediation tracking.

Assessments in OSCAL are expressed in the context of:

- a specific system implementation,
- and a defined set of controls.

OSCAL supports both continuous and periodic (snapshot) assessment modes.

### Assessment Plan Model

Defines how and when assessment activities are performed, including scope and planned assessment actions.

### Assessment Results Model

Captures results produced by assessment activities, including scope, timing, evidence, and findings.

### POA&M Model

Represents findings that require remediation and supports tracking by system owners and maintainers.

## Information Traceability and Data Flow

OSCAL models provide native traceability across layers through explicit import mechanisms.

At a high level:

- controls are defined in catalogs,
- selected and tailored in profiles,
- implemented in SSP/component artifacts,
- evaluated in assessment plan/results,
- and tracked for remediation in POA&M artifacts.

This establishes consistent lineage from assessment findings back to original control definitions.

## Model Lifecycle Status

OSCAL models may move through readiness states such as:

- Future
- Early Access Draft
- Draft
- Prototype
- Pre-Final
- Released

As models mature, schema and reference artifacts are published for XML, JSON, and JSON/YAML validation workflows.

## Current Release State Summary

The following models are currently represented as released in this summary:

- **Control**: Catalog, Profile, Control Mapping
- **Implementation**: Component Definition, System Security Plan
- **Assessment**: Assessment Plan, Assessment Results, POA&M

Where available, schema support is provided as XML and JSON (with JSON schema commonly used for YAML validation workflows).