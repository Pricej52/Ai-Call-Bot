from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.twilio_client import TwilioClient
from app.services.twilio_integrations import get_runtime_twilio_credentials


@dataclass
class TwilioInboundEvent:
    call_sid: str
    from_number: str
    to_number: str
    call_status: str


class TwilioAdapter:
    """Twilio-specific logic is isolated here to keep providers swappable."""

    @staticmethod
    def parse_inbound_webhook(form_data: dict) -> TwilioInboundEvent:
        return TwilioInboundEvent(
            call_sid=form_data.get("CallSid", ""),
            from_number=form_data.get("From", ""),
            to_number=form_data.get("To", ""),
            call_status=form_data.get("CallStatus", "ringing"),
        )


class TenantScopedTwilioProvider:
    @staticmethod
    async def for_tenant(db: AsyncSession, tenant_id: str) -> TwilioClient | None:
        credentials = await get_runtime_twilio_credentials(db, tenant_id)
        if not credentials:
            return None
        account_sid, auth_token = credentials
        return TwilioClient(account_sid, auth_token)
