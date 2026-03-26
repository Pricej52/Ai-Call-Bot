from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.twilio_client import TwilioClient, TwilioClientError
from app.core.config import settings
from app.models import IntegrationStatus, PhoneNumber, TenantIntegration
from app.services.crypto import decrypt_secret, encrypt_secret


def _mask_secret(secret: str) -> str:
    if len(secret) <= 4:
        return "*" * len(secret)
    return f"{'*' * (len(secret) - 4)}{secret[-4:]}"


async def get_tenant_twilio_connection(db: AsyncSession, tenant_id: str) -> TenantIntegration | None:
    result = await db.execute(select(TenantIntegration).where(TenantIntegration.tenant_id == UUID(tenant_id)))
    return result.scalar_one_or_none()


async def upsert_tenant_twilio_connection(
    db: AsyncSession,
    tenant_id: str,
    account_sid: str,
    auth_token: str,
    default_phone_number: str | None,
) -> TenantIntegration:
    existing = await get_tenant_twilio_connection(db, tenant_id)
    if existing:
        existing.account_sid = account_sid
        existing.encrypted_auth_token = encrypt_secret(auth_token)
        existing.masked_auth_token = _mask_secret(auth_token)
        existing.default_phone_number = default_phone_number
        existing.status = IntegrationStatus.not_configured
        existing.metadata_json = {}
        integration = existing
    else:
        integration = TenantIntegration(
            tenant_id=UUID(tenant_id),
            provider="twilio",
            account_sid=account_sid,
            encrypted_auth_token=encrypt_secret(auth_token),
            masked_auth_token=_mask_secret(auth_token),
            default_phone_number=default_phone_number,
            status=IntegrationStatus.not_configured,
        )
        db.add(integration)

    await db.commit()
    await db.refresh(integration)
    return integration


async def update_tenant_twilio_connection(
    db: AsyncSession,
    tenant_id: str,
    account_sid: str | None = None,
    auth_token: str | None = None,
    default_phone_number: str | None = None,
) -> TenantIntegration | None:
    existing = await get_tenant_twilio_connection(db, tenant_id)
    if not existing:
        return None

    if account_sid:
        existing.account_sid = account_sid
    if auth_token:
        existing.encrypted_auth_token = encrypt_secret(auth_token)
        existing.masked_auth_token = _mask_secret(auth_token)
    existing.default_phone_number = default_phone_number
    existing.status = IntegrationStatus.not_configured
    await db.commit()
    await db.refresh(existing)
    return existing


async def disconnect_tenant_twilio_connection(db: AsyncSession, tenant_id: str) -> bool:
    existing = await get_tenant_twilio_connection(db, tenant_id)
    if not existing:
        return False
    await db.delete(existing)
    await db.commit()
    return True


async def test_tenant_twilio_connection(
    db: AsyncSession,
    tenant_id: str,
    include_numbers: bool = True,
) -> dict:
    integration = await get_tenant_twilio_connection(db, tenant_id)
    if not integration:
        return {"status": IntegrationStatus.not_configured, "message": "Twilio is not configured for this tenant."}

    client = TwilioClient(integration.account_sid, decrypt_secret(integration.encrypted_auth_token))

    try:
        account = await client.validate_credentials()
        numbers = await client.list_incoming_numbers() if include_numbers else []
        integration.status = IntegrationStatus.connected
        integration.last_tested_at = datetime.now(timezone.utc)
        integration.metadata_json = {"account_friendly_name": account.get("friendly_name", "")}
        await db.commit()
        await db.refresh(integration)
        return {
            "status": IntegrationStatus.connected,
            "message": "Twilio connection successful.",
            "account_name": account.get("friendly_name") or account.get("sid"),
            "numbers": [n["phone_number"] for n in numbers],
            "last_tested_at": integration.last_tested_at,
        }
    except TwilioClientError:
        integration.status = IntegrationStatus.failed
        integration.last_tested_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(integration)
        return {
            "status": IntegrationStatus.failed,
            "message": "Twilio credentials failed validation. Please verify SID/token.",
            "numbers": [],
            "last_tested_at": integration.last_tested_at,
        }


async def list_tenant_twilio_numbers(db: AsyncSession, tenant_id: str) -> list[str]:
    integration = await get_tenant_twilio_connection(db, tenant_id)
    if not integration:
        return []

    client = TwilioClient(integration.account_sid, decrypt_secret(integration.encrypted_auth_token))
    try:
        numbers = await client.list_incoming_numbers()
        return [n["phone_number"] for n in numbers]
    except TwilioClientError:
        return []


async def sync_tenant_phone_numbers(
    db: AsyncSession,
    tenant_id: str,
    client_account_id: str,
    numbers: list[str],
) -> None:
    tenant_uuid = UUID(tenant_id)
    client_uuid = UUID(client_account_id)

    for number in numbers:
        existing = (
            await db.execute(
                select(PhoneNumber).where(PhoneNumber.tenant_id == tenant_uuid, PhoneNumber.e164_number == number)
            )
        ).scalar_one_or_none()
        if existing:
            existing.is_active = True
            continue

        db.add(
            PhoneNumber(
                tenant_id=tenant_uuid,
                client_account_id=client_uuid,
                e164_number=number,
                provider="twilio",
                is_active=True,
            )
        )
    await db.commit()


async def get_runtime_twilio_credentials(db: AsyncSession, tenant_id: str) -> tuple[str, str] | None:
    integration = await get_tenant_twilio_connection(db, tenant_id)
    if integration:
        return integration.account_sid, decrypt_secret(integration.encrypted_auth_token)

    if settings.twilio_account_sid and settings.twilio_auth_token:
        return settings.twilio_account_sid, settings.twilio_auth_token
    return None
