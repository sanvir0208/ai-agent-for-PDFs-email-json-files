from pydantic import BaseModel
from typing import Optional

class WebhookPayload(BaseModel):
    event_type: str
    timestamp: str
    source: str
    payload: dict
    status: Optional[str] = "received"
