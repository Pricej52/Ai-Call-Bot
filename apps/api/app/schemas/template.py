from pydantic import BaseModel

from app.models.entities import AgentType
from app.schemas.common import BaseReadSchema


class AgentTemplateCreate(BaseModel):
    tenant_id: str
    name: str
    description: str | None = None
    type: AgentType


class AgentTemplateRead(BaseReadSchema):
    tenant_id: str
    name: str
    description: str | None
    type: AgentType
