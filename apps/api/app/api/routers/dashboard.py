from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.crud import get_dashboard_stats

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats")
async def dashboard_stats_route(tenant_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    return await get_dashboard_stats(db, tenant_id)
