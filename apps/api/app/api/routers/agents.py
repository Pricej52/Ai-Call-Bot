from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.agent import AgentCreate, AgentRead
from app.services.crud import create_agent, list_agents

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("", response_model=AgentRead)
async def create_agent_route(payload: AgentCreate, db: AsyncSession = Depends(get_db)):
    model_payload = payload.model_dump()
    for key in ["tenant_id", "client_account_id", "phone_number_id", "template_id"]:
        if model_payload.get(key):
            model_payload[key] = UUID(model_payload[key])
    return await create_agent(db, model_payload)


@router.get("", response_model=list[AgentRead])
async def list_agents_route(tenant_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    return await list_agents(db, tenant_id)
