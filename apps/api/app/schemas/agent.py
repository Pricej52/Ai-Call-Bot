from typing import Any

from pydantic import BaseModel, Field

from app.models.entities import AgentType
from app.schemas.common import BaseReadSchema


class AgentCreate(BaseModel):
    tenant_id: str
    client_account_id: str
    type: AgentType
    name: str
    phone_number_id: str | None = None
    template_id: str | None = None
    language: str = "en"
    voice: str = "alloy"
    voice_settings: dict[str, Any] = Field(default_factory=dict)
    call_flow: dict[str, Any] = Field(default_factory=dict)
    meeting_settings: dict[str, Any] = Field(default_factory=dict)
    twilio_phone_number: str | None = None
    base_prompt: str | None = None
    talk_tracks: str | None = None
    cta_instructions: str | None = None
    voicemail_behavior: str | None = None
    webhook_url: str | None = None
    business_hours: dict[str, Any] = Field(default_factory=dict)
    status: str = "draft"


class AgentRead(BaseReadSchema):
    tenant_id: str
    client_account_id: str
    type: AgentType
    name: str
    language: str
    voice: str
    voice_settings: dict
    call_flow: dict
    meeting_settings: dict
    is_published: bool
    phone_number_id: str | None
    twilio_phone_number: str | None
    base_prompt: str | None
    talk_tracks: str | None
    cta_instructions: str | None
    voicemail_behavior: str | None
    webhook_url: str | None
    business_hours: dict[str, Any]
    status: str
