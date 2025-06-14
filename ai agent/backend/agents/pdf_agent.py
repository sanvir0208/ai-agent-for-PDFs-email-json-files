import pdfplumber
from backend.schemas.pdf_schema import PDFInvoiceSchema
from pydantic import ValidationError
import re

def extract_pdf_fields(file_path: str) -> dict:
    """
    Extract key fields from invoice-style PDF using pdfplumber for text extraction.
    Validate extracted data using PDFInvoiceSchema.
    """
    result = {
        "valid": False,
        "fields": {},
        "anomalies": []
    }

    try:
        full_text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                full_text += page.extract_text() or ""

        # Extract total amount using regex (example patterns)
        total = 0.0
        total_match = re.search(r"(Total|Amount Due|Grand Total)\D*([\d,]+\.\d{2})", full_text, re.IGNORECASE)
        if total_match:
            amount_str = total_match.group(2).replace(",", "")
            total = float(amount_str)

        # Compliance flags check (example keywords)
        lower_text = full_text.lower()
        compliance_flags = []
        if "unauthorized" in lower_text:
            compliance_flags.append("unauthorized_charge")
        if "missing gst" in lower_text:
            compliance_flags.append("missing_gst")
        if "late fee" in lower_text:
            compliance_flags.append("late_fee")

        payload = {
            "total": total,
            "text": full_text,
            "compliance_flags": compliance_flags
        }

        validated = PDFInvoiceSchema(**payload)
        result["valid"] = True
        result["fields"] = validated.dict()

    except ValidationError as e:
        result["anomalies"].extend([err["msg"] for err in e.errors()])
    except Exception as e:
        result["anomalies"].append(str(e))

    return result
