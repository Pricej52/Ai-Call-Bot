from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.wizard import WizardDraftRead, WizardDraftUpsert
from app.services.crud import upsert_wizard_draft

router = APIRouter(prefix="/agent-wizard", tags=["agent-wizard"])


@router.put("/draft", response_model=WizardDraftRead)
async def upsert_wizard_draft_route(payload: WizardDraftUpsert, db: AsyncSession = Depends(get_db)):
    return await upsert_wizard_draft(db, payload.model_dump())
