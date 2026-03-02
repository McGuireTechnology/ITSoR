from sqlalchemy.orm import Session

from itsor.domain.models import PlatformTenant
from itsor.domain.ports.tenant_repository import TenantRepository
from itsor.infrastructure.adapters.sqlalchemy_base_repository import SQLAlchemyBaseRepository
from itsor.infrastructure.models.sqlalchemy_tenant_model import TenantModel


class SQLAlchemyTenantRepository(SQLAlchemyBaseRepository[PlatformTenant, TenantModel], TenantRepository):
    model_class = TenantModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Tenant")

    def _to_domain(self, record: TenantModel) -> PlatformTenant:
        return PlatformTenant(
            id=record.id,
            name=record.name,
            owner_id=record.owner_id,
            group_id=record.group_id,
            permissions=record.permissions,
        )

    def _to_model(self, tenant: PlatformTenant) -> TenantModel:
        return TenantModel(
            id=tenant.id,
            name=tenant.name,
            owner_id=tenant.owner_id,
            group_id=tenant.group_id,
            permissions=tenant.permissions,
        )

    def _apply_updates(self, record: TenantModel, tenant: PlatformTenant) -> None:
        record.name = tenant.name
        record.owner_id = tenant.owner_id
        record.group_id = tenant.group_id
        record.permissions = tenant.permissions

    def get_by_name(self, name: str) -> PlatformTenant | None:
        record = self._db.query(TenantModel).filter(TenantModel.name == name).first()
        return self._to_domain(record) if record else None
