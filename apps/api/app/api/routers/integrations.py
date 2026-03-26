from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import verify_tenant_access, verify_tenant_access_value
from app.db.session import get_db
from app.schemas.integration import (
    TwilioConnectionRead,
    TwilioConnectionTestRequest,
    TwilioConnectionTestResponse,
    TwilioConnectionUpdate,
    TwilioConnectionUpsert,
    TwilioPhoneNumbersResponse,
)
from app.services.twilio_integrations import (
    disconnect_tenant_twilio_connection,
    get_tenant_twilio_connection,
    list_tenant_twilio_numbers,
    sync_tenant_phone_numbers,
    test_tenant_twilio_connection,
    update_tenant_twilio_connection,
    upsert_tenant_twilio_connection,
)

router = APIRouter(prefix="/integrations", tags=["integrations"])


def _as_read(model) -> TwilioConnectionRead:
    return TwilioConnectionRead(
        tenant_id=str(model.tenant_id),
        provider=model.provider,
        account_sid=model.account_sid,
        masked_auth_token=model.masked_auth_token,
        status=model.status.value if hasattr(model.status, "value") else str(model.status),
        default_phone_number=model.default_phone_number,
        metadata_json=model.metadata_json or {},
        last_tested_at=model.last_tested_at,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


@router.get("/twilio", response_model=TwilioConnectionRead | None)
async def get_twilio_integration(
    tenant_id: str = Query(...),
    _: str = Depends(verify_tenant_access),
    db: AsyncSession = Depends(get_db),
):
    found = await get_tenant_twilio_connection(db, tenant_id)
    if not found:
        return None
    return _as_read(found)


@router.post("/twilio", response_model=TwilioConnectionRead)
async def save_twilio_integration(
    payload: TwilioConnectionUpsert,
    x_tenant_id: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
):
    verify_tenant_access_value(payload.tenant_id, x_tenant_id)
    saved = await upsert_tenant_twilio_connection(
        db,
        tenant_id=payload.tenant_id,
        account_sid=payload.account_sid,
        auth_token=payload.auth_token,
        default_phone_number=payload.default_phone_number,
    )
    return _as_read(saved)


@router.patch("/twilio", response_model=TwilioConnectionRead)
async def update_twilio_integration(
    payload: TwilioConnectionUpdate,
    x_tenant_id: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
):
    verify_tenant_access_value(payload.tenant_id, x_tenant_id)
    updated = await update_tenant_twilio_connection(
        db,
        tenant_id=payload.tenant_id,
        account_sid=payload.account_sid,
        auth_token=payload.auth_token,
        default_phone_number=payload.default_phone_number,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Twilio integration not found")
    return _as_read(updated)


@router.delete("/twilio")
async def disconnect_twilio_integration(
    tenant_id: str = Query(...),
    _: str = Depends(verify_tenant_access),
    db: AsyncSession = Depends(get_db),
):
    deleted = await disconnect_tenant_twilio_connection(db, tenant_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Twilio integration not found")
    return {"ok": True}


@router.post("/twilio/test", response_model=TwilioConnectionTestResponse)
async def test_twilio_integration(
    payload: TwilioConnectionTestRequest,
    x_tenant_id: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
):
    verify_tenant_access_value(payload.tenant_id, x_tenant_id)
    result = await test_tenant_twilio_connection(db, payload.tenant_id, include_numbers=payload.include_numbers)
    return TwilioConnectionTestResponse(**result)


@router.get("/twilio/phone-numbers", response_model=TwilioPhoneNumbersResponse)
async def list_twilio_phone_numbers(
    tenant_id: str = Query(...),
    client_account_id: str = Query(...),
    sync_to_tenant_pool: bool = Query(default=True),
    _: str = Depends(verify_tenant_access),
    db: AsyncSession = Depends(get_db),
):
    numbers = await list_tenant_twilio_numbers(db, tenant_id)
    if sync_to_tenant_pool and numbers:
        await sync_tenant_phone_numbers(db, tenant_id, client_account_id, numbers)
    return TwilioPhoneNumbersResponse(tenant_id=tenant_id, numbers=numbers)
