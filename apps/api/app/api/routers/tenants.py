from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.tenant import TenantCreate, TenantRead
from app.services.crud import create_tenant, list_tenants

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("", response_model=TenantRead)
async def create_tenant_route(payload: TenantCreate, db: AsyncSession = Depends(get_db)):
    return await create_tenant(db, payload.name, payload.white_label_domain)


@router.get("", response_model=list[TenantRead])
async def list_tenants_route(db: AsyncSession = Depends(get_db)):
    return await list_tenants(db)
