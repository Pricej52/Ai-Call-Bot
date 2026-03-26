import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.common import TimestampMixin, UUIDMixin


class AgentType(str, Enum):
    inbound = "inbound"
    outbound = "outbound"


class CallDirection(str, Enum):
    inbound = "inbound"
    outbound = "outbound"


class CampaignStatus(str, Enum):
    draft = "draft"
    active = "active"
    paused = "paused"
    completed = "completed"


class IntegrationStatus(str, Enum):
    not_configured = "not_configured"
    connected = "connected"
    failed = "failed"


class Tenant(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    white_label_domain: Mapped[str | None] = mapped_column(String(255))

    users: Mapped[list["TenantUser"]] = relationship(back_populates="tenant")
    clients: Mapped[list["ClientAccount"]] = relationship(back_populates="tenant")
    integrations: Mapped[list["TenantIntegration"]] = relationship(back_populates="tenant")


class TenantUser(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tenant_users"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="admin", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    tenant: Mapped["Tenant"] = relationship(back_populates="users")


class ClientAccount(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "client_accounts"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    industry: Mapped[str | None] = mapped_column(String(120))
    timezone: Mapped[str] = mapped_column(String(80), default="UTC", nullable=False)

    tenant: Mapped["Tenant"] = relationship(back_populates="clients")


class PhoneNumber(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "phone_numbers"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    client_account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("client_accounts.id", ondelete="CASCADE"), nullable=False)
    e164_number: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    provider: Mapped[str] = mapped_column(String(50), default="twilio", nullable=False)
    provider_sid: Mapped[str | None] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class TenantIntegration(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tenant_integrations"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, unique=True)
    provider: Mapped[str] = mapped_column(String(50), default="twilio", nullable=False)
    account_sid: Mapped[str] = mapped_column(String(64), nullable=False)
    encrypted_auth_token: Mapped[str] = mapped_column(Text, nullable=False)
    masked_auth_token: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[IntegrationStatus] = mapped_column(
        SQLEnum(IntegrationStatus),
        default=IntegrationStatus.not_configured,
        nullable=False,
    )
    default_phone_number: Mapped[str | None] = mapped_column(String(30))
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    last_tested_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    tenant: Mapped["Tenant"] = relationship(back_populates="integrations")


class AgentTemplate(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "agent_templates"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    type: Mapped[AgentType] = mapped_column(SQLEnum(AgentType), nullable=False)


class AgentInstance(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "agent_instances"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    client_account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("client_accounts.id", ondelete="CASCADE"), nullable=False)
    template_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("agent_templates.id", ondelete="SET NULL"))
    phone_number_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("phone_numbers.id", ondelete="SET NULL"))
    type: Mapped[AgentType] = mapped_column(SQLEnum(AgentType), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    language: Mapped[str] = mapped_column(String(20), default="en", nullable=False)
    voice: Mapped[str] = mapped_column(String(80), default="alloy", nullable=False)
    voice_settings: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    call_flow: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    meeting_settings: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class PromptVersion(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "prompt_versions"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    agent_instance_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("agent_instances.id", ondelete="CASCADE"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    base_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    industry_prompt: Mapped[str | None] = mapped_column(Text)
    client_prompt: Mapped[str | None] = mapped_column(Text)
    agent_prompt: Mapped[str | None] = mapped_column(Text)
    campaign_instructions: Mapped[str | None] = mapped_column(Text)


class TalkTrack(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "talk_tracks"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    agent_instance_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("agent_instances.id", ondelete="CASCADE"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    tracks: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)


class CTARule(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "cta_rules"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    agent_instance_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("agent_instances.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    condition: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    action: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)


class KnowledgeSource(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "knowledge_sources"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    agent_instance_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("agent_instances.id", ondelete="CASCADE"), nullable=False)
    source_type: Mapped[str] = mapped_column(String(30), default="url", nullable=False)
    source_uri: Mapped[str] = mapped_column(Text, nullable=False)
    retrieval_provider: Mapped[str] = mapped_column(String(80), default="native", nullable=False)
    extra_metadata: Mapped[dict] = mapped_column("metadata", JSONB, default=dict, nullable=False)


class WebhookIntegration(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "webhook_integrations"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    client_account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("client_accounts.id", ondelete="CASCADE"), nullable=False)
    agent_instance_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("agent_instances.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    target_url: Mapped[str] = mapped_column(Text, nullable=False)
    secret: Mapped[str | None] = mapped_column(String(255))
    event_types: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)


class Campaign(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "campaigns"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    client_account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("client_accounts.id", ondelete="CASCADE"), nullable=False)
    agent_instance_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("agent_instances.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[CampaignStatus] = mapped_column(SQLEnum(CampaignStatus), default=CampaignStatus.draft, nullable=False)
    retry_policy: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    business_hours: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)


class CampaignLead(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "campaign_leads"

    campaign_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    external_id: Mapped[str | None] = mapped_column(String(255))
    first_name: Mapped[str | None] = mapped_column(String(120))
    last_name: Mapped[str | None] = mapped_column(String(120))
    phone_number: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str | None] = mapped_column(String(320))
    extra_metadata: Mapped[dict] = mapped_column("metadata", JSONB, default=dict, nullable=False)


class CallSession(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "call_sessions"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    client_account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("client_accounts.id", ondelete="CASCADE"), nullable=False)
    agent_instance_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("agent_instances.id", ondelete="CASCADE"), nullable=False)
    campaign_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("campaigns.id", ondelete="SET NULL"))
    lead_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("campaign_leads.id", ondelete="SET NULL"))
    direction: Mapped[CallDirection] = mapped_column(SQLEnum(CallDirection), nullable=False)
    provider_call_sid: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    from_number: Mapped[str] = mapped_column(String(30), nullable=False)
    to_number: Mapped[str] = mapped_column(String(30), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(40), default="initiated", nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    disposition: Mapped[str | None] = mapped_column(String(120))
    next_action: Mapped[str | None] = mapped_column(String(255))


class TranscriptEntry(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "transcript_entries"

    call_session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("call_sessions.id", ondelete="CASCADE"), nullable=False)
    speaker: Mapped[str] = mapped_column(String(40), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_metadata: Mapped[dict] = mapped_column("metadata", JSONB, default=dict, nullable=False)


class WebhookDelivery(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "webhook_deliveries"

    integration_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("webhook_integrations.id", ondelete="CASCADE"), nullable=False)
    call_session_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("call_sessions.id", ondelete="SET NULL"))
    payload: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    response_status: Mapped[int | None] = mapped_column(Integer)
    response_body: Mapped[str | None] = mapped_column(Text)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AgentWizardDraft(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "agent_wizard_drafts"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    client_account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("client_accounts.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenant_users.id", ondelete="CASCADE"), nullable=False)
    step: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
