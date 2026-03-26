from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class TwilioConnectionUpsert(BaseModel):
    tenant_id: str
    account_sid: str
    auth_token: str
    default_phone_number: str | None = None


class TwilioConnectionUpdate(BaseModel):
    tenant_id: str
    account_sid: str | None = None
    auth_token: str | None = None
    default_phone_number: str | None = None


class TwilioConnectionRead(BaseModel):
    tenant_id: str
    provider: str
    account_sid: str
    masked_auth_token: str
    status: str
    default_phone_number: str | None
    metadata_json: dict[str, Any] = Field(default_factory=dict)
    last_tested_at: datetime | None
    created_at: datetime
    updated_at: datetime


class TwilioConnectionTestRequest(BaseModel):
    tenant_id: str
    include_numbers: bool = True


class TwilioConnectionTestResponse(BaseModel):
    status: str
    message: str
    account_name: str | None = None
    numbers: list[str] = Field(default_factory=list)
    last_tested_at: datetime | None = None


class TwilioPhoneNumbersResponse(BaseModel):
    tenant_id: str
    numbers: list[str] = Field(default_factory=list)
