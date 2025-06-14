# backend/utils.py

import re
import json

def clean_text(text: str) -> str:
    """Remove extra whitespace and non-printable characters from text."""
    text = re.sub(r'\s+', ' ', text)  # collapse multiple whitespace to single space
    text = text.strip()
    return text

def is_json(text: str) -> bool:
    """Check if a string is a valid JSON."""
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False

def extract_email_subject(text: str) -> str:
    """Simple extraction of email subject line."""
    match = re.search(r'Subject:\s*(.*)', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "No Subject Found"

def extract_invoice_number(text: str) -> str:
    """Dummy extraction of invoice number from PDF text."""
    match = re.search(r'Invoice Number[:\s]+(\w+)', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "No Invoice Number Found"
