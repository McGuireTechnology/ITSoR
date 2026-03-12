from fastapi import APIRouter, Depends, HTTPException, Query, status

from itsor.api.deps import get_current_user, get_oscal_document_use_cases
from itsor.api.schemas.oscal import OscalDocumentCreate, OscalDocumentReplace, OscalDocumentResponse
from itsor.application.use_cases.oscal import OscalDocumentUseCases


router = APIRouter(prefix="/documents", tags=["oscal"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[OscalDocumentResponse])
def read_oscal_documents(
    document_type: str | None = Query(default=None, description="Optional OSCAL document type filter."),
    use_cases: OscalDocumentUseCases = Depends(get_oscal_document_use_cases),
):
    try:
        return use_cases.list_documents(document_type=document_type)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/{document_id}", response_model=OscalDocumentResponse)
def read_oscal_document(document_id: str, use_cases: OscalDocumentUseCases = Depends(get_oscal_document_use_cases)):
    document = use_cases.get_document(document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OSCAL document not found")
    return document


@router.post("/", response_model=OscalDocumentResponse, status_code=status.HTTP_201_CREATED)
def create_oscal_document(body: OscalDocumentCreate, use_cases: OscalDocumentUseCases = Depends(get_oscal_document_use_cases)):
    try:
        return use_cases.create_document(
            document_type=body.document_type,
            content_json=body.content_json,
            title=body.title,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.put("/{document_id}", response_model=OscalDocumentResponse)
def replace_oscal_document(
    document_id: str,
    body: OscalDocumentReplace,
    use_cases: OscalDocumentUseCases = Depends(get_oscal_document_use_cases),
):
    try:
        return use_cases.replace_document(
            document_id=document_id,
            document_type=body.document_type,
            content_json=body.content_json,
            title=body.title,
        )
    except ValueError as exc:
        message = str(exc)
        code = status.HTTP_404_NOT_FOUND if "not found" in message.lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=message)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_oscal_document(document_id: str, use_cases: OscalDocumentUseCases = Depends(get_oscal_document_use_cases)):
    try:
        use_cases.delete_document(document_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return None
