from dataclasses import dataclass
from typing import Any, cast

import ulid

from itsor.application.ports.oscal import OscalDocumentRepository
from itsor.domain.models.oscal import (
    OscalAssessmentPlanDocument,
    OscalAssessmentResultsDocument,
    OscalCatalogDocument,
    OscalComponentDefinitionDocument,
    OscalMappingDocument,
    OscalPoamDocument,
    OscalProfileDocument,
    OscalSystemSecurityPlanDocument,
)


OSCAL_DOCUMENT_VALIDATORS: dict[str, type] = {
    "catalog": OscalCatalogDocument,
    "profile": OscalProfileDocument,
    "mapping": OscalMappingDocument,
    "assessment-plan": OscalAssessmentPlanDocument,
    "assessment-results": OscalAssessmentResultsDocument,
    "poam": OscalPoamDocument,
    "component-definition": OscalComponentDefinitionDocument,
    "system-security-plan": OscalSystemSecurityPlanDocument,
}


@dataclass
class OscalStoredDocument:
    id: str
    document_type: str
    content_json: dict[str, Any]
    title: str | None = None


class OscalDocumentUseCases:
    def __init__(self, repo: OscalDocumentRepository) -> None:
        self._repo = repo

    def list_documents(self, document_type: str | None = None) -> list[Any]:
        if document_type is None:
            return self._repo.list()
        normalized = self._normalize_document_type(document_type)
        return self._repo.list_by_document_type(normalized)

    def get_document(self, document_id: str) -> Any | None:
        return self._repo.get_by_id(document_id)

    def create_document(
        self,
        *,
        document_type: str,
        content_json: dict[str, Any],
        title: str | None = None,
    ) -> Any:
        normalized = self._normalize_document_type(document_type)
        canonical_content = self._validate_document(normalized, content_json)
        document = OscalStoredDocument(
            id=str(ulid.new()),
            document_type=normalized,
            content_json=canonical_content,
            title=title,
        )
        return self._repo.create(document)

    def replace_document(
        self,
        *,
        document_id: str,
        document_type: str,
        content_json: dict[str, Any],
        title: str | None = None,
    ) -> Any:
        existing = self._repo.get_by_id(document_id)
        if existing is None:
            raise ValueError("OSCAL document not found")
        normalized = self._normalize_document_type(document_type)
        canonical_content = self._validate_document(normalized, content_json)
        existing.document_type = normalized
        existing.content_json = canonical_content
        existing.title = title
        return self._repo.update(existing)

    def delete_document(self, document_id: str) -> None:
        existing = self._repo.get_by_id(document_id)
        if existing is None:
            raise ValueError("OSCAL document not found")
        self._repo.delete(document_id)

    def _normalize_document_type(self, document_type: str) -> str:
        normalized = document_type.strip().lower()
        if normalized not in OSCAL_DOCUMENT_VALIDATORS:
            allowed = ", ".join(sorted(OSCAL_DOCUMENT_VALIDATORS.keys()))
            raise ValueError(f"Unsupported OSCAL document type '{document_type}'. Allowed types: {allowed}")
        return normalized

    def _validate_document(self, document_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        validator = OSCAL_DOCUMENT_VALIDATORS[document_type]
        try:
            validated = cast(Any, validator).model_validate(payload)
        except Exception as exc:
            raise ValueError(f"Invalid OSCAL {document_type} document: {exc}") from exc
        dumped: dict[str, Any] = validated.model_dump(by_alias=True, exclude_none=True)
        return dumped
