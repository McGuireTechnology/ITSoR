from itsor.api.routes.oscal._submodule import build_oscal_submodule_router


router = build_oscal_submodule_router(
    prefix="/poams",
    tag="oscal.poams",
    document_type="poam",
)


__all__ = ["router"]