from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    AgentInstance,
    AgentWizardDraft,
    CallSession,
    Campaign,
    ClientAccount,
    PhoneNumber,
    Tenant,
    TranscriptEntry,
)


def _normalize_number(number: str | None) -> str | None:
    if not number:
        return None
    return number.replace(" ", "").replace("-", "")


async def create_tenant(db: AsyncSession, name: str, white_label_domain: str | None) -> Tenant:
    tenant = Tenant(name=name, white_label_domain=white_label_domain)
    db.add(tenant)
    await db.commit()
    await db.refresh(tenant)
    return tenant


async def list_tenants(db: AsyncSession) -> list[Tenant]:
    result = await db.execute(select(Tenant).order_by(Tenant.created_at.desc()))
    return list(result.scalars().all())


async def create_client(db: AsyncSession, tenant_id: str, name: str, industry: str | None, timezone: str) -> ClientAccount:
    client = ClientAccount(tenant_id=UUID(tenant_id), name=name, industry=industry, timezone=timezone)
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client


async def list_clients(db: AsyncSession, tenant_id: str) -> list[ClientAccount]:
    result = await db.execute(select(ClientAccount).where(ClientAccount.tenant_id == UUID(tenant_id)))
    return list(result.scalars().all())


async def _resolve_phone_number(
    db: AsyncSession,
    tenant_id: UUID,
    client_account_id: UUID,
    twilio_phone_number: str | None,
) -> UUID | None:
    normalized_number = _normalize_number(twilio_phone_number)
    if not normalized_number:
        return None

    existing = (
        await db.execute(
            select(PhoneNumber).where(
                PhoneNumber.e164_number == normalized_number,
                PhoneNumber.tenant_id == tenant_id,
            )
        )
    ).scalar_one_or_none()

    if existing:
        return existing.id

    phone_number = PhoneNumber(
        tenant_id=tenant_id,
        client_account_id=client_account_id,
        e164_number=normalized_number,
        provider="twilio",
        is_active=True,
    )
    db.add(phone_number)
    await db.flush()
    return phone_number.id


def _sync_agent_config(payload: dict) -> None:
    call_flow = payload.setdefault("call_flow", {})

    explicit_fields = {
        "base_prompt": payload.pop("base_prompt", None),
        "talk_tracks": payload.pop("talk_tracks", None),
        "cta_instructions": payload.pop("cta_instructions", None),
        "voicemail_behavior": payload.pop("voicemail_behavior", None),
        "webhook_url": payload.pop("webhook_url", None),
        "business_hours": payload.pop("business_hours", None),
    }

    for key, value in explicit_fields.items():
        if value is not None:
            call_flow[key] = value

    if "status" in payload:
        payload["is_published"] = payload.pop("status") == "published"


async def create_agent(db: AsyncSession, payload: dict) -> AgentInstance:
    _sync_agent_config(payload)

    tenant_id = payload["tenant_id"]
    client_account_id = payload["client_account_id"]

    twilio_phone_number = payload.pop("twilio_phone_number", None)
    if twilio_phone_number and not payload.get("phone_number_id"):
        payload["phone_number_id"] = await _resolve_phone_number(db, tenant_id, client_account_id, twilio_phone_number)

    agent = AgentInstance(**payload)
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    return agent


async def update_agent(db: AsyncSession, agent_id: str, payload: dict) -> AgentInstance | None:
    result = await db.execute(select(AgentInstance).where(AgentInstance.id == UUID(agent_id)))
    agent = result.scalar_one_or_none()
    if not agent:
        return None

    mutable_payload = dict(payload)
    _sync_agent_config(mutable_payload)

    twilio_phone_number = mutable_payload.pop("twilio_phone_number", None)
    if twilio_phone_number:
        mutable_payload["phone_number_id"] = await _resolve_phone_number(
            db, agent.tenant_id, agent.client_account_id, twilio_phone_number
        )

    for key, value in mutable_payload.items():
        setattr(agent, key, value)

    await db.commit()
    await db.refresh(agent)
    return agent


async def delete_agent(db: AsyncSession, agent_id: str) -> bool:
    result = await db.execute(select(AgentInstance).where(AgentInstance.id == UUID(agent_id)))
    agent = result.scalar_one_or_none()
    if not agent:
        return False

    await db.delete(agent)
    await db.commit()
    return True


async def get_agent(db: AsyncSession, agent_id: str) -> AgentInstance | None:
    result = await db.execute(select(AgentInstance).where(AgentInstance.id == UUID(agent_id)))
    return result.scalar_one_or_none()


async def list_agents(db: AsyncSession, tenant_id: str) -> list[AgentInstance]:
    result = await db.execute(
        select(AgentInstance)
        .where(AgentInstance.tenant_id == UUID(tenant_id))
        .order_by(AgentInstance.created_at.desc())
    )
    return list(result.scalars().all())


async def upsert_wizard_draft(db: AsyncSession, payload: dict) -> AgentWizardDraft:
    query = select(AgentWizardDraft).where(
        AgentWizardDraft.tenant_id == UUID(payload["tenant_id"]),
        AgentWizardDraft.client_account_id == UUID(payload["client_account_id"]),
        AgentWizardDraft.user_id == UUID(payload["user_id"]),
    )
    found = (await db.execute(query)).scalar_one_or_none()
    if found:
        found.step = payload["step"]
        found.payload = payload["payload"]
        draft = found
    else:
        draft = AgentWizardDraft(
            tenant_id=UUID(payload["tenant_id"]),
            client_account_id=UUID(payload["client_account_id"]),
            user_id=UUID(payload["user_id"]),
            step=payload["step"],
            payload=payload["payload"],
        )
        db.add(draft)

    await db.commit()
    await db.refresh(draft)
    return draft


async def create_call_session(db: AsyncSession, payload: dict) -> CallSession:
    call = CallSession(**payload)
    db.add(call)
    await db.commit()
    await db.refresh(call)
    return call


async def get_call_by_provider_sid(db: AsyncSession, provider_call_sid: str) -> CallSession | None:
    result = await db.execute(select(CallSession).where(CallSession.provider_call_sid == provider_call_sid))
    return result.scalar_one_or_none()


async def update_call_status(
    db: AsyncSession,
    provider_call_sid: str,
    status: str,
    ended_at: datetime | None = None,
    disposition: str | None = None,
) -> CallSession | None:
    call = await get_call_by_provider_sid(db, provider_call_sid)
    if not call:
        return None

    call.status = status
    if ended_at:
        call.ended_at = ended_at
    if disposition:
        call.disposition = disposition

    await db.commit()
    await db.refresh(call)
    return call


async def list_calls(db: AsyncSession, tenant_id: str) -> list[CallSession]:
    result = await db.execute(
        select(CallSession)
        .where(CallSession.tenant_id == UUID(tenant_id))
        .order_by(CallSession.started_at.desc())
    )
    return list(result.scalars().all())


async def get_call(db: AsyncSession, call_id: str) -> CallSession | None:
    result = await db.execute(select(CallSession).where(CallSession.id == UUID(call_id)))
    return result.scalar_one_or_none()


async def list_transcript_entries(db: AsyncSession, call_id: str) -> list[TranscriptEntry]:
    result = await db.execute(
        select(TranscriptEntry)
        .where(TranscriptEntry.call_session_id == UUID(call_id))
        .order_by(TranscriptEntry.sequence.asc())
    )
    return list(result.scalars().all())


async def append_transcript_entry(
    db: AsyncSession,
    call_session_id: UUID,
    speaker: str,
    content: str,
    extra_metadata: dict | None = None,
) -> TranscriptEntry:
    current_sequence = (
        await db.execute(
            select(func.coalesce(func.max(TranscriptEntry.sequence), 0)).where(
                TranscriptEntry.call_session_id == call_session_id
            )
        )
    ).scalar_one()

    entry = TranscriptEntry(
        call_session_id=call_session_id,
        speaker=speaker,
        content=content,
        sequence=int(current_sequence) + 1,
        extra_metadata=extra_metadata or {},
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


async def get_dashboard_stats(db: AsyncSession, tenant_id: str) -> dict[str, int]:
    tenant_uuid = UUID(tenant_id)

    total_agents = (
        await db.execute(select(func.count()).select_from(AgentInstance).where(AgentInstance.tenant_id == tenant_uuid))
    ).scalar_one()
    total_calls = (
        await db.execute(select(func.count()).select_from(CallSession).where(CallSession.tenant_id == tenant_uuid))
    ).scalar_one()
    total_campaigns = (
        await db.execute(select(func.count()).select_from(Campaign).where(Campaign.tenant_id == tenant_uuid))
    ).scalar_one()

    return {
        "total_agents": int(total_agents),
        "total_calls": int(total_calls),
        "total_campaigns": int(total_campaigns),
    }
