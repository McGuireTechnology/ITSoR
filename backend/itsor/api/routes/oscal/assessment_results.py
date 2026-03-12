from itsor.api.routes.oscal._submodule import build_oscal_submodule_router


router = build_oscal_submodule_router(
    prefix="/assessment-results",
    tag="oscal.assessment-results",
    document_type="assessment-results",
)


__all__ = ["router"]