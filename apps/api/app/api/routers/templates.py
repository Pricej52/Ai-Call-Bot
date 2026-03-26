from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import AgentTemplate
from app.schemas.template import AgentTemplateCreate, AgentTemplateRead

router = APIRouter(prefix="/agent-templates", tags=["agent-templates"])


@router.post("", response_model=AgentTemplateRead)
async def create_template_route(payload: AgentTemplateCreate, db: AsyncSession = Depends(get_db)):
    template = AgentTemplate(
        tenant_id=UUID(payload.tenant_id),
        name=payload.name,
        description=payload.description,
        type=payload.type,
    )
    db.add(template)
    await db.commit()
    await db.refresh(template)
    return template


@router.get("", response_model=list[AgentTemplateRead])
async def list_templates_route(tenant_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AgentTemplate).where(AgentTemplate.tenant_id == UUID(tenant_id)))
    return list(result.scalars().all())


@router.get("/{template_id}", response_model=AgentTemplateRead)
async def get_template_route(template_id: str, db: AsyncSession = Depends(get_db)):
    template = (await db.execute(select(AgentTemplate).where(AgentTemplate.id == UUID(template_id)))).scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Agent template not found")
    return template


@router.patch("/{template_id}", response_model=AgentTemplateRead)
async def update_template_route(template_id: str, payload: dict, db: AsyncSession = Depends(get_db)):
    template = (await db.execute(select(AgentTemplate).where(AgentTemplate.id == UUID(template_id)))).scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Agent template not found")

    for key in ["name", "description", "type"]:
        if key in payload:
            setattr(template, key, payload[key])

    await db.commit()
    await db.refresh(template)
    return template
