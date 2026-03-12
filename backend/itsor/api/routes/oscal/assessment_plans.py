from itsor.api.routes.oscal._submodule import build_oscal_submodule_router


router = build_oscal_submodule_router(
    prefix="/assessment-plans",
    tag="oscal.assessment-plans",
    document_type="assessment-plan",
)


__all__ = ["router"]