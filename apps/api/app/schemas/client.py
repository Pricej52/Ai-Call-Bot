from pydantic import BaseModel

from app.schemas.common import BaseReadSchema


class ClientCreate(BaseModel):
    tenant_id: str
    name: str
    industry: str | None = None
    timezone: str = "UTC"


class ClientRead(BaseReadSchema):
    tenant_id: str
    name: str
    industry: str | None
    timezone: str
