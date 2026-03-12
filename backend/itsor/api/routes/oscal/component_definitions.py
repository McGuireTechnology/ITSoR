from itsor.api.routes.oscal._submodule import build_oscal_submodule_router


router = build_oscal_submodule_router(
    prefix="/component-definitions",
    tag="oscal.component-definitions",
    document_type="component-definition",
)


__all__ = ["router"]