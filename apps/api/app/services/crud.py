from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AgentInstance, AgentWizardDraft, CallSession, ClientAccount, Tenant


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


async def create_agent(db: AsyncSession, payload: dict) -> AgentInstance:
    agent = AgentInstance(**payload)
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    return agent


async def list_agents(db: AsyncSession, tenant_id: str) -> list[AgentInstance]:
    result = await db.execute(select(AgentInstance).where(AgentInstance.tenant_id == UUID(tenant_id)))
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
