from typing import Any

from pydantic import BaseModel

from app.schemas.common import BaseReadSchema


class WizardDraftUpsert(BaseModel):
    tenant_id: str
    client_account_id: str
    user_id: str
    step: int
    payload: dict[str, Any]


class WizardDraftRead(BaseReadSchema):
    tenant_id: str
    client_account_id: str
    user_id: str
    step: int
    payload: dict
