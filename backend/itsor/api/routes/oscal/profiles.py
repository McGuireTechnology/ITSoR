from itsor.api.routes.oscal._submodule import build_oscal_submodule_router


router = build_oscal_submodule_router(
    prefix="/profiles",
    tag="oscal.profiles",
    document_type="profile",
)


__all__ = ["router"]