from pydantic import BaseModel, EmailStr

from app.schemas.common import BaseReadSchema


class TenantCreate(BaseModel):
    name: str
    white_label_domain: str | None = None


class TenantRead(BaseReadSchema):
    name: str
    white_label_domain: str | None


class TenantUserCreate(BaseModel):
    tenant_id: str
    email: EmailStr
    password: str
    full_name: str
    role: str = "admin"
