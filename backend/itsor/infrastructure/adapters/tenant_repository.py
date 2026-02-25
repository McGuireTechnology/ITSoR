from typing import Optional, List

from sqlalchemy.orm import Session

from itsor.domain.models.tenant import Tenant
from itsor.domain.ports.tenant_repository import TenantRepository
from itsor.infrastructure.models.tenant import TenantModel


class SQLAlchemyTenantRepository(TenantRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def _to_domain(self, record: TenantModel) -> Tenant:
        return Tenant(
            id=record.id,
            name=record.name,
        )

    def _to_model(self, tenant: Tenant) -> TenantModel:
        return TenantModel(
            id=tenant.id,
            name=tenant.name,
        )

    def get_by_id(self, tenant_id: str) -> Optional[Tenant]:
        record = self._db.query(TenantModel).filter(TenantModel.id == tenant_id).first()
        return self._to_domain(record) if record else None

    def get_by_name(self, name: str) -> Optional[Tenant]:
        record = self._db.query(TenantModel).filter(TenantModel.name == name).first()
        return self._to_domain(record) if record else None

    def list(self) -> List[Tenant]:
        records = self._db.query(TenantModel).all()
        return [self._to_domain(r) for r in records]

    def create(self, tenant: Tenant) -> Tenant:
        record = self._to_model(tenant)
        self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return self._to_domain(record)

    def update(self, tenant: Tenant) -> Tenant:
        record = self._db.query(TenantModel).filter(TenantModel.id == tenant.id).first()
        if not record:
            raise ValueError(f"Tenant {tenant.id} not found")
        record.name = tenant.name
        self._db.commit()
        self._db.refresh(record)
        return self._to_domain(record)

    def delete(self, tenant_id: str) -> None:
        record = self._db.query(TenantModel).filter(TenantModel.id == tenant_id).first()
        if record:
            self._db.delete(record)
            self._db.commit()
