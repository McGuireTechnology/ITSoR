from itsor.api.routes.oscal._submodule import build_oscal_submodule_router


router = build_oscal_submodule_router(
    prefix="/system-security-plans",
    tag="oscal.system-security-plans",
    document_type="system-security-plan",
)


__all__ = ["router"]