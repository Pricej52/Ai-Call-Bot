from datetime import datetime

from pydantic import BaseModel

from app.models.entities import CallDirection
from app.schemas.common import BaseReadSchema


class CallSessionCreate(BaseModel):
    tenant_id: str
    client_account_id: str
    agent_instance_id: str
    direction: CallDirection
    provider_call_sid: str
    from_number: str
    to_number: str
    started_at: datetime
    status: str = "initiated"


class CallSessionRead(BaseReadSchema):
    tenant_id: str
    client_account_id: str
    agent_instance_id: str
    direction: CallDirection
    provider_call_sid: str
    from_number: str
    to_number: str
    started_at: datetime
    ended_at: datetime | None
    status: str
    summary: str | None
    disposition: str | None
    next_action: str | None


class TranscriptEntryRead(BaseReadSchema):
    call_session_id: str
    speaker: str
    content: str
    sequence: int
    extra_metadata: dict


class CallWithTranscriptRead(CallSessionRead):
    transcript_entries: list[TranscriptEntryRead]
