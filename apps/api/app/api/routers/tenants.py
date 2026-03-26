from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Tenant
from app.schemas.tenant import TenantCreate, TenantRead
from app.services.crud import create_tenant, list_tenants

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("", response_model=TenantRead)
async def create_tenant_route(payload: TenantCreate, db: AsyncSession = Depends(get_db)):
    return await create_tenant(db, payload.name, payload.white_label_domain)


@router.get("", response_model=list[TenantRead])
async def list_tenants_route(db: AsyncSession = Depends(get_db)):
    return await list_tenants(db)


@router.get("/{tenant_id}", response_model=TenantRead)
async def get_tenant_route(tenant_id: str, db: AsyncSession = Depends(get_db)):
    tenant = (await db.execute(select(Tenant).where(Tenant.id == UUID(tenant_id)))).scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@router.patch("/{tenant_id}", response_model=TenantRead)
async def update_tenant_route(tenant_id: str, payload: dict, db: AsyncSession = Depends(get_db)):
    tenant = (await db.execute(select(Tenant).where(Tenant.id == UUID(tenant_id)))).scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    if "name" in payload:
        tenant.name = payload["name"]
    if "white_label_domain" in payload:
        tenant.white_label_domain = payload["white_label_domain"]

    await db.commit()
    await db.refresh(tenant)
    return tenant
