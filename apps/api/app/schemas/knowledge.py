from pydantic import BaseModel, Field

from app.schemas.common import BaseReadSchema


class KnowledgeSourceCreate(BaseModel):
    tenant_id: str
    agent_instance_id: str
    source_type: str = "url"
    source_uri: str
    retrieval_provider: str = "native"
    extra_metadata: dict = Field(default_factory=dict)


class KnowledgeSourceRead(BaseReadSchema):
    tenant_id: str
    agent_instance_id: str
    source_type: str
    source_uri: str
    retrieval_provider: str
    extra_metadata: dict
