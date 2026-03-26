from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import AgentInstance, PhoneNumber
from app.schemas.agent import AgentCreate, AgentRead
from app.services.crud import create_agent, delete_agent, get_agent, list_agents, update_agent

router = APIRouter(prefix="/agents", tags=["agents"])


def _extract_config(agent: AgentInstance) -> dict:
    flow = agent.call_flow or {}
    return {
        "base_prompt": flow.get("base_prompt") or flow.get("prompt"),
        "talk_tracks": flow.get("talk_tracks"),
        "cta_instructions": flow.get("cta_instructions") or flow.get("cta", {}).get("text"),
        "voicemail_behavior": flow.get("voicemail_behavior") or flow.get("voicemail", {}).get("message"),
        "webhook_url": flow.get("webhook_url"),
        "business_hours": flow.get("business_hours", {}),
    }


async def _to_agent_read(agent: AgentInstance, db: AsyncSession) -> AgentRead:
    phone_number = None
    if agent.phone_number_id:
        phone_number = (
            await db.execute(select(PhoneNumber).where(PhoneNumber.id == agent.phone_number_id))
        ).scalar_one_or_none()

    config = _extract_config(agent)

    return AgentRead(
        id=str(agent.id),
        created_at=agent.created_at,
        updated_at=agent.updated_at,
        tenant_id=str(agent.tenant_id),
        client_account_id=str(agent.client_account_id),
        type=agent.type,
        name=agent.name,
        language=agent.language,
        voice=agent.voice,
        voice_settings=agent.voice_settings,
        call_flow=agent.call_flow,
        meeting_settings=agent.meeting_settings,
        is_published=agent.is_published,
        phone_number_id=str(agent.phone_number_id) if agent.phone_number_id else None,
        twilio_phone_number=phone_number.e164_number if phone_number else None,
        base_prompt=config["base_prompt"],
        talk_tracks=config["talk_tracks"],
        cta_instructions=config["cta_instructions"],
        voicemail_behavior=config["voicemail_behavior"],
        webhook_url=config["webhook_url"],
        business_hours=config["business_hours"],
        status="published" if agent.is_published else "draft",
    )


@router.post("", response_model=AgentRead)
async def create_agent_route(payload: AgentCreate, db: AsyncSession = Depends(get_db)):
    model_payload = payload.model_dump(exclude_unset=True)
    for key in ["tenant_id", "client_account_id", "phone_number_id", "template_id"]:
        if model_payload.get(key):
            model_payload[key] = UUID(model_payload[key])

    created = await create_agent(db, model_payload)
    return await _to_agent_read(created, db)


@router.get("", response_model=list[AgentRead])
async def list_agents_route(tenant_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    agents = await list_agents(db, tenant_id)
    return [await _to_agent_read(agent, db) for agent in agents]


@router.get("/{agent_id}", response_model=AgentRead)
async def get_agent_route(agent_id: str, db: AsyncSession = Depends(get_db)):
    agent = await get_agent(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return await _to_agent_read(agent, db)


@router.patch("/{agent_id}", response_model=AgentRead)
async def update_agent_route(agent_id: str, payload: dict, db: AsyncSession = Depends(get_db)):
    parsed_payload = dict(payload)
    for key in ["tenant_id", "client_account_id", "phone_number_id", "template_id"]:
        if parsed_payload.get(key):
            parsed_payload[key] = UUID(parsed_payload[key])

    updated = await update_agent(db, agent_id, parsed_payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Agent not found")

    return await _to_agent_read(updated, db)


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent_route(agent_id: str, db: AsyncSession = Depends(get_db)):
    deleted = await delete_agent(db, agent_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Agent not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
