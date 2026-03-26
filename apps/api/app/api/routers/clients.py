from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.client import ClientCreate, ClientRead
from app.services.crud import create_client, list_clients

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("", response_model=ClientRead)
async def create_client_route(payload: ClientCreate, db: AsyncSession = Depends(get_db)):
    return await create_client(db, payload.tenant_id, payload.name, payload.industry, payload.timezone)


@router.get("", response_model=list[ClientRead])
async def list_clients_route(tenant_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    return await list_clients(db, tenant_id)
