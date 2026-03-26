from fastapi import Header, HTTPException


async def verify_tenant_access(tenant_id: str, x_tenant_id: str | None = Header(default=None)) -> str:
    if x_tenant_id and x_tenant_id != tenant_id:
        raise HTTPException(status_code=403, detail="Tenant access denied")
    return tenant_id


def verify_tenant_access_value(tenant_id: str, request_tenant_id: str | None) -> str:
    if request_tenant_id and request_tenant_id != tenant_id:
        raise HTTPException(status_code=403, detail="Tenant access denied")
    return tenant_id
