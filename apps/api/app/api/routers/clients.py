from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import ClientAccount
from app.schemas.client import ClientCreate, ClientRead
from app.services.crud import create_client, list_clients

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("", response_model=ClientRead)
async def create_client_route(payload: ClientCreate, db: AsyncSession = Depends(get_db)):
    return await create_client(db, payload.tenant_id, payload.name, payload.industry, payload.timezone)


@router.get("", response_model=list[ClientRead])
async def list_clients_route(tenant_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    return await list_clients(db, tenant_id)


@router.get("/{client_id}", response_model=ClientRead)
async def get_client_route(client_id: str, db: AsyncSession = Depends(get_db)):
    client = (await db.execute(select(ClientAccount).where(ClientAccount.id == UUID(client_id)))).scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.patch("/{client_id}", response_model=ClientRead)
async def update_client_route(client_id: str, payload: dict, db: AsyncSession = Depends(get_db)):
    client = (await db.execute(select(ClientAccount).where(ClientAccount.id == UUID(client_id)))).scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    for key in ["name", "industry", "timezone"]:
        if key in payload:
            setattr(client, key, payload[key])

    await db.commit()
    await db.refresh(client)
    return client
