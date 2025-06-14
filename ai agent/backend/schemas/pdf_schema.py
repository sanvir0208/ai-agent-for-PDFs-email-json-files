from pydantic import BaseModel
from typing import List

class PDFInvoiceSchema(BaseModel):
    total: float
    text: str
    compliance_flags: List[str]
