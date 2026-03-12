from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from itsor.application.use_cases.oscal import OscalDocumentUseCases
from itsor.infrastructure.adapters.sqlalchemy.oscal_repository import InMemoryOscalDocumentRepository


def _metadata() -> dict[str, object]:
    return {
        "title": "Sample",
        "last-modified": datetime.now(UTC).isoformat(),
        "version": "1.0.0",
        "oscal-version": "1.2.1",
    }


def _payloads() -> dict[str, dict[str, object]]:
    return {
        "catalog": {
            "catalog": {
                "uuid": str(uuid4()),
                "metadata": _metadata(),
            }
        },
        "profile": {
            "profile": {
                "uuid": str(uuid4()),
                "metadata": _metadata(),
                "imports": [{"href": "https://example.org/catalog.json", "include-all": {}}],
            }
        },
        "mapping": {
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
                    "source-resource": {"type": "catalog", "href": "https://example.org/source-catalog.json"},
                    "target-resource": {"type": "catalog", "href": "https://example.org/target-catalog.json"},
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
        },
        "assessment-plan": {
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
            }
        },
        "assessment-results": {
            "assessment-results": {
                "uuid": str(uuid4()),
                "metadata": _metadata(),
                "import-ap": {"href": "https://example.org/ap.json"},
                "results": [
                    {
                        "uuid": str(uuid4()),
                        "title": "Initial Assessment Result",
                        "description": "Summary",
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
            }
        },
        "poam": {
            "plan-of-action-and-milestones": {
                "uuid": str(uuid4()),
                "metadata": _metadata(),
                "poam-items": [
                    {
                        "title": "POA&M Item 1",
                        "description": "Track remediation",
                    }
                ],
            }
        },
        "component-definition": {
            "component-definition": {
                "uuid": str(uuid4()),
                "metadata": _metadata(),
                "components": [
                    {
                        "uuid": str(uuid4()),
                        "type": "software",
                        "title": "Sample Component",
                        "description": "Implements selected controls.",
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
            }
        },
        "system-security-plan": {
            "system-security-plan": {
                "uuid": str(uuid4()),
                "metadata": _metadata(),
                "system-characteristics": {
                    "system-name": "ITSoR Demo System",
                },
            }
        },
    }


@pytest.mark.parametrize("document_type", sorted(_payloads().keys()))
def test_oscal_use_case_accepts_all_document_types(document_type: str) -> None:
    repo = InMemoryOscalDocumentRepository()
    use_cases = OscalDocumentUseCases(repo)
    payload = _payloads()[document_type]

    created = use_cases.create_document(
        document_type=document_type,
        content_json=payload,
        title=f"{document_type} test",
    )

    assert created.document_type == document_type
    assert created.title == f"{document_type} test"

    listed = use_cases.list_documents(document_type=document_type)
    assert len(listed) == 1
    assert listed[0].id == created.id


def test_oscal_use_case_rejects_unknown_document_type() -> None:
    repo = InMemoryOscalDocumentRepository()
    use_cases = OscalDocumentUseCases(repo)

    with pytest.raises(ValueError, match="Unsupported OSCAL document type"):
        use_cases.create_document(
            document_type="not-a-type",
            content_json={"dummy": {}},
        )
