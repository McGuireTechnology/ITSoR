# OSCAL Control Layer: Catalog Model

## Purpose

The OSCAL catalog model represents a collection of controls as a control catalog.

It standardizes how control definitions from different sources (for example, NIST SP 800-53, ISO/IEC 27002, and COBIT) are represented in machine-readable formats, which makes control content easier to search, import, export, and process consistently across tools.

While primarily designed for security and privacy controls, the same approach may be applicable to other domains.

## Catalog Schemas and Converters

The catalog model is commonly exchanged and validated in these encodings:

- JSON (with JSON Schema)
- XML (with XML Schema)
- YAML (typically validated via JSON schema workflows)

Typical conversion workflows include:

- XML to JSON conversion
- JSON to XML conversion

## Authors and Consumers

### Catalog Authors

- Compliance framework and requirements authors
- Organizations defining new controls not present in existing catalogs

### Catalog Consumers

Because the catalog is foundational in OSCAL, consumers include users of downstream artifacts such as:

- baseline/profile authors and consumers,
- component definition authors and consumers,
- SSP authors and consumers,
- auditors and authorizing officials.

## Catalog Organization

An OSCAL catalog follows the standard OSCAL document pattern:

- **Metadata**: required in all OSCAL models; includes document title, publication version/date, OSCAL version, and participant/role/location information.
- **Parameter**: defines parameters reused across multiple control requirement statements.
- **Control**: contains control-specific requirements, parameters, objectives, assessment methods, references, and subordinate controls.
- **Group**: organizes related controls and related group-level parameters.
- **Back Matter**: shared syntax for attachments, citations, and embedded content.

## Key Concepts

The catalog model is used in two major ways:

1. To represent a complete control set from an authoritative source in machine-readable form.
2. To represent the output of profile resolution so consumers can process baseline-resolved controls in one unified structure.

Across these uses, the catalog model supports:

- grouping related controls;
- defining control statements;
- parameterization;
- implementation guidance;
- objectives;
- assessment methods;
- related-control relationships;
- references.

## Important Note to Developers

Whenever OSCAL file content changes:

1. Generate and assign a new root-level `uuid`.
2. Update `metadata.last-modified` to the save time of the modified content.

These values let tools detect changed content efficiently. During format conversion (for example, XML to JSON), these values should remain unchanged so tools can determine the content is equivalent across formats.

## Content Examples

NIST maintains OSCAL examples for SP 800-53 control catalogs (including Rev. 4 and Rev. 5) in XML, JSON, and YAML formats in the OSCAL content repository.

Additional stakeholders also publish OSCAL catalogs and baselines for other control regimes.