from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_current_user, get_oscal_document_use_cases
from itsor.api.schemas.oscal import OscalDocumentResponse, OscalSubmoduleUpsert
from itsor.application.use_cases.oscal import OscalDocumentUseCases


def build_oscal_submodule_router(*, prefix: str, tag: str, document_type: str) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=[tag], dependencies=[Depends(get_current_user)])

    @router.get("/", response_model=list[OscalDocumentResponse])
    def _read_documents(use_cases: OscalDocumentUseCases = Depends(get_oscal_document_use_cases)):
        return use_cases.list_documents(document_type=document_type)

    @router.get("/{document_id}", response_model=OscalDocumentResponse)
    def _read_document(document_id: str, use_cases: OscalDocumentUseCases = Depends(get_oscal_document_use_cases)):
        document = use_cases.get_document(document_id)
        if document is None or getattr(document, "document_type", None) != document_type:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OSCAL document not found")
        return document

    @router.post("/", response_model=OscalDocumentResponse, status_code=status.HTTP_201_CREATED)
    def _create_document(
        body: OscalSubmoduleUpsert,
        use_cases: OscalDocumentUseCases = Depends(get_oscal_document_use_cases),
    ):
        try:
            return use_cases.create_document(
                document_type=document_type,
                content_json=body.content_json,
                title=body.title,
            )
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    @router.put("/{document_id}", response_model=OscalDocumentResponse)
    def _replace_document(
        document_id: str,
        body: OscalSubmoduleUpsert,
        use_cases: OscalDocumentUseCases = Depends(get_oscal_document_use_cases),
    ):
        document = use_cases.get_document(document_id)
        if document is None or getattr(document, "document_type", None) != document_type:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OSCAL document not found")
        try:
            return use_cases.replace_document(
                document_id=document_id,
                document_type=document_type,
                content_json=body.content_json,
                title=body.title,
            )
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    @router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
    def _delete_document(document_id: str, use_cases: OscalDocumentUseCases = Depends(get_oscal_document_use_cases)):
        document = use_cases.get_document(document_id)
        if document is None or getattr(document, "document_type", None) != document_type:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OSCAL document not found")
        use_cases.delete_document(document_id)
        return None

    _ = (_read_documents, _read_document, _create_document, _replace_document, _delete_document)

    return router


__all__ = ["build_oscal_submodule_router"]