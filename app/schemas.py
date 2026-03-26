from pydantic import BaseModel, Field


class TwilioInboundWebhookPayload(BaseModel):
    CallSid: str = Field(..., description="Twilio Call SID")
    From: str = Field(..., description="Caller E.164 number")
    To: str = Field(..., description="Recipient Twilio E.164 number")
    CallStatus: str = Field(default="ringing")


class OutboundCallJobRequest(BaseModel):
    to_number: str
    from_number: str


class CallSessionResponse(BaseModel):
    id: int
    call_sid: str | None
    direction: str
    from_number: str
    to_number: str
    agent_id: int | None
    status: str


class OutboundCallJobResponse(BaseModel):
    id: int
    status: str
    provider_call_sid: str | None
    call_session_id: int
