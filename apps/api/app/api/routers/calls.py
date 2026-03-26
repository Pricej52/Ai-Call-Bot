from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.twilio import TwilioAdapter
from app.db.session import get_db
from app.models import AgentInstance, CallDirection, PhoneNumber
from app.schemas.call import CallSessionRead
from app.services.crud import create_call_session

router = APIRouter(prefix="/calls", tags=["calls"])


@router.post("/webhooks/twilio/inbound", response_model=CallSessionRead)
async def twilio_inbound_webhook(
    CallSid: str = Form(...),
    From: str = Form(...),
    To: str = Form(...),
    CallStatus: str = Form("ringing"),
    db: AsyncSession = Depends(get_db),
):
    event = TwilioAdapter.parse_inbound_webhook(
        {"CallSid": CallSid, "From": From, "To": To, "CallStatus": CallStatus}
    )

    phone = (
        await db.execute(select(PhoneNumber).where(PhoneNumber.e164_number == event.to_number, PhoneNumber.is_active.is_(True)))
    ).scalar_one_or_none()
    if not phone:
        raise HTTPException(status_code=404, detail="No phone number configuration found")

    agent = (
        await db.execute(
            select(AgentInstance).where(
                AgentInstance.phone_number_id == phone.id,
                AgentInstance.type == "inbound",
                AgentInstance.is_published.is_(True),
            )
        )
    ).scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="No published inbound agent for number")

    call_payload = {
        "tenant_id": phone.tenant_id,
        "client_account_id": phone.client_account_id,
        "agent_instance_id": agent.id,
        "campaign_id": None,
        "lead_id": None,
        "direction": CallDirection.inbound,
        "provider_call_sid": event.call_sid,
        "from_number": event.from_number,
        "to_number": event.to_number,
        "started_at": datetime.now(timezone.utc),
        "status": event.call_status,
    }

    return await create_call_session(db, call_payload)
