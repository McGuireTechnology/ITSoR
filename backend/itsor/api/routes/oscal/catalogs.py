from itsor.api.routes.oscal._submodule import build_oscal_submodule_router


router = build_oscal_submodule_router(
    prefix="/catalogs",
    tag="oscal.catalogs",
    document_type="catalog",
)


__all__ = ["router"]