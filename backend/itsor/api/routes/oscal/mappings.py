from itsor.api.routes.oscal._submodule import build_oscal_submodule_router


router = build_oscal_submodule_router(
    prefix="/mappings",
    tag="oscal.mappings",
    document_type="mapping",
)


__all__ = ["router"]