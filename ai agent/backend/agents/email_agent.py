from email import message_from_string

from backend.schemas.email_schema import EmailSchema
from pydantic import ValidationError

def extract_email_fields(raw_email: str) -> dict:
    """
    Parses raw email text, extracts key fields, and validates with EmailSchema.
    """
    result = {
        "valid": False,
        "fields": {},
        "anomalies": []
    }
    try:
        msg = message_from_string(raw_email)
        from_addr = msg.get('From', '')
        to_addr = msg.get('To', '')
        subject = msg.get('Subject', '')

        
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    payload = part.get_payload(decode=True)
                    if isinstance(payload, bytes):
                        body = payload.decode(part.get_content_charset('utf-8'), errors='ignore')
                    else:
                        body = payload
                    break
        else:
            payload = msg.get_payload(decode=True)
            if isinstance(payload, bytes):
                body = payload.decode(msg.get_content_charset('utf-8'), errors='ignore')
            else:
                body = payload

        payload = {
            "from_addr": from_addr,
            "to_addr": to_addr,
            "subject": subject,
            "body": body
        }

        validated = EmailSchema(**payload)
        result["valid"] = True
        result["fields"] = validated.dict()

    except ValidationError as e:
        result["anomalies"].extend([err["msg"] for err in e.errors()])
    except Exception as e:
        result["anomalies"].append(str(e))

    return result
