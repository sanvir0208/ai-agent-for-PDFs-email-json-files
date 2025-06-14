from pydantic import BaseModel
from typing import Literal

class ClassifierSchema(BaseModel):
    format: Literal["email", "json", "pdf"]
    intent: Literal["RFQ", "Complaint", "Invoice", "Regulation", "Fraud Risk"]
