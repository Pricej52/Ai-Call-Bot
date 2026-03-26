from datetime import datetime, timezone
from xml.sax.saxutils import escape

from fastapi import APIRouter, Depends, Form, HTTPException, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.llm import LLMOrchestratorAdapter
from app.adapters.twilio import TwilioAdapter
from app.db.session import get_db
from app.models import AgentInstance, CallDirection, PhoneNumber
from app.schemas.call import CallSessionRead, CallWithTranscriptRead
from app.services.crud import (
    append_transcript_entry,
    create_call_session,
    get_call,
    get_call_by_provider_sid,
    list_calls,
    list_transcript_entries,
    update_call_status,
)

router = APIRouter(prefix="/calls", tags=["calls"])


def _build_system_prompt(agent: AgentInstance) -> str:
    flow = agent.call_flow or {}
    sections = [
        "You are a helpful phone intake assistant. Keep responses concise, conversational, and phone-friendly.",
        f"Language: {agent.language}",
    ]
    if flow.get("base_prompt"):
        sections.append(f"Base prompt: {flow['base_prompt']}")
    if flow.get("talk_tracks"):
        sections.append(f"Talk tracks / objections: {flow['talk_tracks']}")
    if flow.get("cta_instructions"):
        sections.append(f"Call-to-action instructions: {flow['cta_instructions']}")
    return "\n".join(sections)


def _twiml_gather(prompt: str, call_sid: str, voice: str = "Polly.Joanna") -> str:
    escaped_prompt = escape(prompt)
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        "<Response>"
        f"<Gather input=\"speech\" action=\"/api/v1/calls/webhooks/twilio/respond?call_sid={escape(call_sid)}\" "
        "method=\"POST\" speechTimeout=\"auto\" timeout=\"5\">"
        f"<Say voice=\"{escape(voice)}\">{escaped_prompt}</Say>"
        "</Gather>"
        "<Say voice=\"Polly.Joanna\">I did not hear anything. Goodbye.</Say>"
        "<Hangup/>"
        "</Response>"
    )


@router.get("", response_model=list[CallSessionRead])
async def list_calls_route(tenant_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    return await list_calls(db, tenant_id)


@router.get("/{call_id}", response_model=CallWithTranscriptRead)
async def get_call_route(call_id: str, db: AsyncSession = Depends(get_db)):
    call = await get_call(db, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")

    transcript_entries = await list_transcript_entries(db, call_id)
    return CallWithTranscriptRead(
        id=call.id,
        created_at=call.created_at,
        updated_at=call.updated_at,
        tenant_id=call.tenant_id,
        client_account_id=call.client_account_id,
        agent_instance_id=call.agent_instance_id,
        direction=call.direction,
        provider_call_sid=call.provider_call_sid,
        from_number=call.from_number,
        to_number=call.to_number,
        started_at=call.started_at,
        ended_at=call.ended_at,
        status=call.status,
        summary=call.summary,
        disposition=call.disposition,
        next_action=call.next_action,
        transcript_entries=transcript_entries,
    )


@router.post("/webhooks/twilio/inbound", response_class=PlainTextResponse)
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
        return PlainTextResponse(
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Say>No active number configuration found.</Say><Hangup/></Response>",
            media_type="application/xml",
        )

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
        return PlainTextResponse(
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Say>No published inbound agent is configured for this number.</Say><Hangup/></Response>",
            media_type="application/xml",
        )

    existing = await get_call_by_provider_sid(db, event.call_sid)
    if not existing:
        await create_call_session(
            db,
            {
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
            },
        )

    greeting = "Hello, thanks for calling. How can I help you today?"
    call_flow = agent.call_flow or {}
    if call_flow.get("base_prompt"):
        greeting = call_flow.get("greeting", greeting)

    return PlainTextResponse(_twiml_gather(greeting, event.call_sid), media_type="application/xml")


@router.post("/webhooks/twilio/respond", response_class=PlainTextResponse)
async def twilio_conversation_turn(
    call_sid: str = Query(...),
    SpeechResult: str = Form(""),
    db: AsyncSession = Depends(get_db),
):
    call = await get_call_by_provider_sid(db, call_sid)
    if not call:
        return PlainTextResponse(
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Say>Call session not found.</Say><Hangup/></Response>",
            media_type="application/xml",
        )

    agent = (
        await db.execute(select(AgentInstance).where(AgentInstance.id == call.agent_instance_id))
    ).scalar_one()

    user_utterance = (SpeechResult or "").strip()
    if user_utterance:
        await append_transcript_entry(db, call.id, "caller", user_utterance)

    lower = user_utterance.lower()
    if any(keyword in lower for keyword in ["goodbye", "bye", "stop", "that's all", "hang up"]):
        await append_transcript_entry(db, call.id, "agent", "Thanks for calling. Goodbye.")
        await update_call_status(
            db,
            provider_call_sid=call_sid,
            status="completed",
            ended_at=datetime.now(timezone.utc),
            disposition="caller_ended",
        )
        return PlainTextResponse(
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Say>Thanks for calling. Goodbye.</Say><Hangup/></Response>",
            media_type="application/xml",
        )

    if not user_utterance:
        follow_up = "I didn't catch that. Could you please repeat your question?"
    else:
        orchestrator = LLMOrchestratorAdapter()
        follow_up = await orchestrator.respond(_build_system_prompt(agent), user_utterance)

    await append_transcript_entry(db, call.id, "agent", follow_up)
    await update_call_status(db, provider_call_sid=call_sid, status="in_progress")

    return PlainTextResponse(_twiml_gather(follow_up, call_sid), media_type="application/xml")


@router.post("/webhooks/twilio/status", response_class=PlainTextResponse)
async def twilio_status_callback(
    CallSid: str = Form(...),
    CallStatus: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    terminal_states = {"completed", "failed", "busy", "no-answer", "canceled"}
    ended_at = datetime.now(timezone.utc) if CallStatus in terminal_states else None
    await update_call_status(db, CallSid, CallStatus, ended_at=ended_at, disposition=CallStatus)
    return PlainTextResponse("ok")
