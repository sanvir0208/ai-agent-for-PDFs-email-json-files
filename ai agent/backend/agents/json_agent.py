import json
from pydantic import ValidationError
from backend.schemas.json_schema import WebhookPayload

def validate_json_schema(content: str) -> dict:
    """
    Validates JSON input against the predefined WebhookPayload schema.
    Returns structured output and flags anomalies.
    """

    try:
        data = json.loads(content)
        validated = WebhookPayload(**data)
        return {
            "valid": True,
            "data": validated.dict(),
            "anomalies": []
        }
    except json.JSONDecodeError as e:
        return {
            "valid": False,
            "data": None,
            "anomalies": [f"Invalid JSON format: {str(e)}"]
        }
    except ValidationError as e:
        return {
            "valid": False,
            "data": None,
            "anomalies": [err['msg'] for err in e.errors()]
        }
