# Key Concepts and Terms Used in OSCAL

This page summarizes foundational OSCAL terminology and groups each concept by the OSCAL layer where it is first introduced.

## OSCAL Layers

### Control Definition

Provides shared, reusable control information that can be used across organizations.

### Implementation

Describes how a system, service, software, or hardware offering implements selected controls.

### Assessment

Captures how controls are evaluated through human activities and automated mechanisms.

## Control Definition Concepts

### Control

A **control** is a requirement or guideline intended to reduce a specific risk to information systems and information.

In practice, controls sit at the center of compliance workflows:

- Framework authors define control requirements.
- System owners implement controls.
- Assessors verify implementation against the requirement.

Controls in OSCAL are represented in the **catalog model**.

### Catalog

A **catalog** is an organized collection of controls.

In OSCAL, catalogs are machine-readable and designed to preserve detailed framework structure, including:

- grouped controls,
- subordinate controls (enhancements),
- objectives and methods for assessment,
- references and framework-specific metadata.

Catalogs may include assessment content directly or separate it depending on framework conventions.

### Baseline (Profile / Overlay)

A **baseline** (also called an overlay in some ecosystems) is a selected set of controls taken from one or more catalogs to support risk management and compliance goals.

In OSCAL, baselines are represented with the **profile model**, which:

- explicitly maps selected controls back to source catalogs,
- supports selection and tailoring,
- can reference multiple catalogs in one profile.

This keeps control selection traceable and machine-readable from source catalog to implementation and assessment artifacts.

## Relationship Summary

- Catalogs define available controls.
- Profiles/baselines select and tailor controls from catalogs.
- Implementations document how selected controls are satisfied.
- Assessments evaluate whether implementations meet control intent.