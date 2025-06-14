from pydantic import BaseModel, EmailStr
from typing import List, Optional

class EmailSchema(BaseModel):
    from_address: EmailStr
    to_addresses: List[EmailStr]
    cc_addresses: Optional[List[EmailStr]] = []
    bcc_addresses: Optional[List[EmailStr]] = []
    subject: str
    body: str
    attachments: Optional[List[str]] = []
