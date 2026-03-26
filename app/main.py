from __future__ import annotations

from fastapi import FastAPI, HTTPException

from app.database import execute, initialize_database
from app.schemas import (
    CallSessionResponse,
    OutboundCallJobRequest,
    OutboundCallJobResponse,
    TwilioInboundWebhookPayload,
)
from app.services import (
    create_call_session,
    find_call_session_by_call_sid,
    get_call_session_by_id,
    resolve_agent_id_by_twilio_number,
    store_call_state_transition,
)
from app.twilio_adapter import MockTwilioVoiceAdapter, TwilioVoiceAdapter

app = FastAPI(title="AI Call Bot Voice Backend")
twilio_adapter: TwilioVoiceAdapter = MockTwilioVoiceAdapter()


@app.on_event("startup")
def startup_event() -> None:
    initialize_database()


@app.post("/webhooks/twilio/voice/inbound", response_model=CallSessionResponse)
def handle_inbound_voice_webhook(payload: TwilioInboundWebhookPayload) -> CallSessionResponse:
    existing = find_call_session_by_call_sid(payload.CallSid)
    if existing:
        prev_status = existing["status"]
        new_status = payload.CallStatus
        if prev_status != new_status:
            store_call_state_transition(
                call_session_id=int(existing["id"]),
                from_state=prev_status,
                to_state=new_status,
                source="twilio_inbound_webhook",
                metadata=payload.model_dump(),
            )
        session = get_call_session_by_id(int(existing["id"]))
        return CallSessionResponse(**session)

    agent_id = resolve_agent_id_by_twilio_number(payload.To)
    if agent_id is None:
        raise HTTPException(status_code=404, detail=f"No active agent mapped to Twilio number {payload.To}")

    call_session_id = create_call_session(
        call_sid=payload.CallSid,
        direction="inbound",
        from_number=payload.From,
        to_number=payload.To,
        agent_id=agent_id,
        status=payload.CallStatus,
        provider="twilio",
    )
    session = get_call_session_by_id(call_session_id)
    return CallSessionResponse(**session)


@app.post("/calls/outbound-jobs", response_model=OutboundCallJobResponse)
def create_outbound_call_job(request: OutboundCallJobRequest) -> OutboundCallJobResponse:
    agent_id = resolve_agent_id_by_twilio_number(request.from_number)
    if agent_id is None:
        raise HTTPException(status_code=404, detail=f"No active agent mapped to Twilio number {request.from_number}")

    result = twilio_adapter.create_outbound_call(
        from_number=request.from_number,
        to_number=request.to_number,
        callback_url="/webhooks/twilio/voice/inbound",
    )
    call_session_id = create_call_session(
        call_sid=result.call_sid,
        direction="outbound",
        from_number=request.from_number,
        to_number=request.to_number,
        agent_id=agent_id,
        status=result.status,
        provider="twilio",
    )

    job_id = execute(
        """
        INSERT INTO outbound_call_jobs (target_number, source_number, agent_id, status, provider_call_sid)
        VALUES (?, ?, ?, ?, ?)
        """,
        (request.to_number, request.from_number, agent_id, result.status, result.call_sid),
    )

    return OutboundCallJobResponse(
        id=job_id,
        status=result.status,
        provider_call_sid=result.call_sid,
        call_session_id=call_session_id,
    )


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
