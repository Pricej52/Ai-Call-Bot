from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BaseReadSchema(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
