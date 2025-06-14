from pydantic import BaseModel, ValidationError
from typing import Optional
import re

class ClassificationSchema(BaseModel):
    format: str  # json, email, pdf, unknown
    intent: Optional[str]  # RFQ, Complaint, Invoice, Regulation, Fraud Risk, etc.

def detect_format_and_intent(filename: str, content: str) -> tuple[str, Optional[str]]:
    # Determine format from filename and content (basic heuristics)
    ext = filename.split('.')[-1].lower()
    if ext in ['json']:
        file_format = 'json'
    elif ext in ['eml', 'txt']:
        file_format = 'email'
    elif ext in ['pdf']:
        file_format = 'pdf'
    else:
        file_format = 'unknown'

    # Intent detection by keywords (very basic)
    intents = {
        "RFQ": r"\brequest for quote\b|\brfq\b",
        "Complaint": r"\bcomplaint\b|\bissue\b|\bproblem\b",
        "Invoice": r"\binvoice\b|\bbill\b",
        "Regulation": r"\bgdpr\b|\bfda\b|\bcompliance\b",
        "Fraud Risk": r"\bfraud\b|\brisk\b|\banomaly\b",
    }

    intent = None
    for key, pattern in intents.items():
        if re.search(pattern, content, re.I):
            intent = key
            break

    # Validate classification data
    try:
        validated = ClassificationSchema(format=file_format, intent=intent)
        return validated.format, validated.intent
    except ValidationError:
        # fallback if validation fails
        return file_format, intent
