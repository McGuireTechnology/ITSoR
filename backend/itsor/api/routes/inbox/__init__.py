from fastapi import APIRouter

from itsor.core.api.routes.auth import router as auth_router
from itsor.core.api.routes.attributes import router as attributes_router
from itsor.core.api.routes.databases import router as databases_router
from itsor.core.api.routes.entities import router as entities_router
from itsor.core.api.routes.groups import router as groups_router
from itsor.core.api.routes.records import router as records_router
from itsor.core.api.routes.schemas import router as schemas_router
from itsor.core.api.routes.tenants import router as tenants_router
from itsor.core.api.routes.users import router as users_router
from itsor.core.api.routes.values import router as values_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(databases_router)
api_router.include_router(schemas_router)
api_router.include_router(entities_router)
api_router.include_router(attributes_router)
api_router.include_router(values_router)
api_router.include_router(records_router)
api_router.include_router(users_router)
api_router.include_router(tenants_router)
api_router.include_router(groups_router)
