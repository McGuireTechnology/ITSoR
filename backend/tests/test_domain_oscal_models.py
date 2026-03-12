from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from itsor.domain.models.oscal.control.catalog import OscalCatalogDocument
from itsor.domain.models.oscal.control.mapping import OscalMappingDocument
from itsor.domain.models.oscal.control.profile import OscalProfileDocument
from itsor.domain.models.oscal.assessment.plan import OscalAssessmentPlanDocument
from itsor.domain.models.oscal.assessment.plan_of_action_and_milestones import OscalPoamDocument
from itsor.domain.models.oscal.assessment.results import OscalAssessmentResultsDocument
from itsor.domain.models.oscal.implementation.compenent import OscalComponentDefinitionDocument
from itsor.domain.models.oscal.implementation.system_security_plan import OscalSystemSecurityPlanDocument


def _metadata() -> dict[str, object]:
    return {
        "title": "Sample",
        "last-modified": datetime.now(UTC).isoformat(),
        "version": "1.0.0",
        "oscal-version": "1.2.1",
    }


def test_oscal_catalog_document_minimal_valid() -> None:
    payload = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "catalog": {
            "uuid": str(uuid4()),
            "metadata": _metadata(),
        },
    }

    document = OscalCatalogDocument.model_validate(payload)

    assert document.catalog.metadata.version == "1.0.0"


def test_oscal_profile_document_minimal_valid() -> None:
    payload = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "profile": {
            "uuid": str(uuid4()),
            "metadata": _metadata(),
            "imports": [
                {
                    "href": "https://example.org/catalog.json",
                    "include-all": {},
                }
            ],
        },
    }

    document = OscalProfileDocument.model_validate(payload)

    assert len(document.profile.imports) == 1


def test_oscal_profile_import_requires_single_include_mode() -> None:
    payload = {
        "profile": {
            "uuid": str(uuid4()),
            "metadata": _metadata(),
            "imports": [
                {
                    "href": "https://example.org/catalog.json",
                    "include-all": {},
                    "include-controls": [{"with-ids": ["ac-1"]}],
                }
            ],
        }
    }

    with pytest.raises(ValueError, match="exactly one of include-all or include-controls"):
        OscalProfileDocument.model_validate(payload)


def test_oscal_mapping_document_minimal_valid() -> None:
    payload = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "mapping-collection": {
            "uuid": str(uuid4()),
            "metadata": _metadata(),
            "provenance": {
                "method": "human",
                "matching-rationale": "semantic",
                "status": "complete",
                "mapping-description": "Sample mapping",
            },
            "mappings": {
                "uuid": str(uuid4()),
                "source-resource": {
                    "type": "catalog",
                    "href": "https://example.org/source-catalog.json",
                },
                "target-resource": {
                    "type": "catalog",
                    "href": "https://example.org/target-catalog.json",
                },
                "maps": [
                    {
                        "uuid": str(uuid4()),
                        "relationship": "subset-of",
                        "sources": [{"type": "control", "id-ref": "ac-1"}],
                        "targets": [{"type": "control", "id-ref": "ctrl-1"}],
                    }
                ],
            },
        },
    }

    document = OscalMappingDocument.model_validate(payload)

    assert document.mapping_collection.provenance.method == "human"


def test_oscal_mapping_confidence_percentage_range() -> None:
    payload = {
        "mapping-collection": {
            "uuid": str(uuid4()),
            "metadata": _metadata(),
            "provenance": {
                "method": "human",
                "matching-rationale": "semantic",
                "status": "complete",
                "mapping-description": "Sample mapping",
                "confidence-score": {"percentage": 1.5},
            },
            "mappings": {
                "uuid": str(uuid4()),
                "source-resource": {
                    "type": "catalog",
                    "href": "https://example.org/source-catalog.json",
                },
                "target-resource": {
                    "type": "catalog",
                    "href": "https://example.org/target-catalog.json",
                },
                "maps": [
                    {
                        "uuid": str(uuid4()),
                        "relationship": "subset-of",
                        "sources": [{"type": "control", "id-ref": "ac-1"}],
                        "targets": [{"type": "control", "id-ref": "ctrl-1"}],
                    }
                ],
            },
        }
    }

    with pytest.raises(ValueError, match="percentage must be between 0 and 1"):
        OscalMappingDocument.model_validate(payload)


def test_oscal_component_definition_document_minimal_valid() -> None:
    payload = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "component-definition": {
            "uuid": str(uuid4()),
            "metadata": _metadata(),
            "components": [
                {
                    "uuid": str(uuid4()),
                    "type": "software",
                    "title": "Sample Component",
                    "description": "Implements selected control capabilities.",
                    "control-implementations": [
                        {
                            "uuid": str(uuid4()),
                            "source": "https://example.org/catalog.json",
                            "description": "Control implementation set.",
                            "implemented-requirements": [
                                {
                                    "uuid": str(uuid4()),
                                    "control-id": "ac-1",
                                    "description": "Implements access control requirement.",
                                }
                            ],
                        }
                    ],
                }
            ],
        },
    }

    document = OscalComponentDefinitionDocument.model_validate(payload)

    assert document.component_definition.components is not None
    assert document.component_definition.components[0].type == "software"


def test_oscal_assessment_plan_document_minimal_valid() -> None:
    payload = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "assessment-plan": {
            "uuid": str(uuid4()),
            "metadata": _metadata(),
            "import-ssp": {"href": "https://example.org/ssp.json"},
            "reviewed-controls": {
                "control-selections": [
                    {
                        "include-all": {},
                    }
                ]
            },
            "assessment-subjects": [{"include-all": {}}],
        },
    }

    document = OscalAssessmentPlanDocument.model_validate(payload)

    assert document.assessment_plan.import_ssp.href == "https://example.org/ssp.json"


def test_oscal_assessment_plan_control_selection_requires_single_include_mode() -> None:
    payload = {
        "assessment-plan": {
            "uuid": str(uuid4()),
            "metadata": _metadata(),
            "import-ssp": {"href": "https://example.org/ssp.json"},
            "reviewed-controls": {
                "control-selections": [
                    {
                        "include-all": {},
                        "include-controls": [{"control-id": "ac-1"}],
                    }
                ]
            },
        },
    }

    with pytest.raises(ValueError, match="exactly one of include-all or include-controls"):
        OscalAssessmentPlanDocument.model_validate(payload)


def test_oscal_assessment_results_document_minimal_valid() -> None:
    payload = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "assessment-results": {
            "uuid": str(uuid4()),
            "metadata": _metadata(),
            "import-ap": {"href": "https://example.org/ap.json"},
            "results": [
                {
                    "uuid": str(uuid4()),
                    "title": "Initial Assessment Result",
                    "description": "Summary of executed assessment activities.",
                    "start": datetime.now(UTC).isoformat(),
                    "reviewed-controls": {
                        "control-selections": [
                            {
                                "include-all": {},
                            }
                        ]
                    },
                }
            ],
        },
    }

    document = OscalAssessmentResultsDocument.model_validate(payload)

    assert document.assessment_results.import_ap.href == "https://example.org/ap.json"


def test_oscal_assessment_results_requires_reviewed_controls() -> None:
    payload = {
        "assessment-results": {
            "uuid": str(uuid4()),
            "metadata": _metadata(),
            "import-ap": {"href": "https://example.org/ap.json"},
            "results": [
                {
                    "uuid": str(uuid4()),
                    "title": "Incomplete Result",
                    "description": "Missing reviewed controls.",
                    "start": datetime.now(UTC).isoformat(),
                }
            ],
        }
    }

    with pytest.raises(ValueError, match="reviewed-controls"):
        OscalAssessmentResultsDocument.model_validate(payload)


def test_oscal_poam_document_minimal_valid() -> None:
    payload = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "plan-of-action-and-milestones": {
            "uuid": str(uuid4()),
            "metadata": _metadata(),
            "poam-items": [
                {
                    "title": "POA&M Item 1",
                    "description": "Track remediation for identified weakness.",
                }
            ],
        },
    }

    document = OscalPoamDocument.model_validate(payload)

    assert len(document.plan_of_action_and_milestones.poam_items) == 1


def test_oscal_poam_requires_poam_items() -> None:
    payload = {
        "plan-of-action-and-milestones": {
            "uuid": str(uuid4()),
            "metadata": _metadata(),
        }
    }

    with pytest.raises(ValueError, match="poam-items"):
        OscalPoamDocument.model_validate(payload)


def test_oscal_system_security_plan_document_minimal_valid() -> None:
    payload = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "system-security-plan": {
            "uuid": str(uuid4()),
            "metadata": _metadata(),
            "system-characteristics": {
                "system-name": "ITSoR Demo System",
            },
        },
    }

    document = OscalSystemSecurityPlanDocument.model_validate(payload)

    assert document.system_security_plan.system_characteristics.system_name == "ITSoR Demo System"