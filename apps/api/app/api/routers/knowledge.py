from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import KnowledgeSource
from app.schemas.knowledge import KnowledgeSourceCreate, KnowledgeSourceRead

router = APIRouter(prefix="/knowledge-sources", tags=["knowledge-sources"])


@router.post("", response_model=KnowledgeSourceRead)
async def create_knowledge_source_route(payload: KnowledgeSourceCreate, db: AsyncSession = Depends(get_db)):
    source = KnowledgeSource(
        tenant_id=UUID(payload.tenant_id),
        agent_instance_id=UUID(payload.agent_instance_id),
        source_type=payload.source_type,
        source_uri=payload.source_uri,
        retrieval_provider=payload.retrieval_provider,
        extra_metadata=payload.extra_metadata,
    )
    db.add(source)
    await db.commit()
    await db.refresh(source)
    return source


@router.get("", response_model=list[KnowledgeSourceRead])
async def list_knowledge_sources_route(agent_instance_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(KnowledgeSource).where(KnowledgeSource.agent_instance_id == UUID(agent_instance_id))
    )
    return list(result.scalars().all())


@router.get("/{source_id}", response_model=KnowledgeSourceRead)
async def get_knowledge_source_route(source_id: str, db: AsyncSession = Depends(get_db)):
    source = (await db.execute(select(KnowledgeSource).where(KnowledgeSource.id == UUID(source_id)))).scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Knowledge source not found")
    return source


@router.patch("/{source_id}", response_model=KnowledgeSourceRead)
async def update_knowledge_source_route(source_id: str, payload: dict, db: AsyncSession = Depends(get_db)):
    source = (await db.execute(select(KnowledgeSource).where(KnowledgeSource.id == UUID(source_id)))).scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Knowledge source not found")

    for key in ["source_type", "source_uri", "retrieval_provider", "extra_metadata"]:
        if key in payload:
            setattr(source, key, payload[key])

    await db.commit()
    await db.refresh(source)
    return source
