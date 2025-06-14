from typing import Dict, Any

def action_router(agent_output: Dict[str, Any]) -> str:
    # Simulate action routing based on agent output
    # For example, escalate complaint with high urgency and angry tone

    if agent_output.get("format") == "email":
        urgency = agent_output.get("email_data", {}).get("urgency", "normal")
        tone = agent_output.get("email_data", {}).get("tone", "neutral")
        intent = agent_output.get("intent", "")

        if intent == "complaint" and urgency == "high" and tone == "angry":
            # Simulate API call to CRM escalate
            return "Action: Escalate to CRM"
        else:
            return "Action: Log and close"

    elif agent_output.get("format") == "json":
        if agent_output.get("json_data", {}).get("valid") is False:
            return "Action: Log alert - JSON anomalies detected"
        return "Action: Process JSON normally"

    elif agent_output.get("format") == "pdf":
        invoice_total = agent_output.get("pdf_data", {}).get("invoice_total", 0)
        mentions = agent_output.get("pdf_data", {}).get("mentions", [])

        if invoice_total > 10000:
            return "Action: Flag high invoice amount"
        if any(word in mentions for word in ["GDPR", "FDA", "HIPAA"]):
            return "Action: Flag compliance risk"
        return "Action: Process PDF normally"

    else:
        return "Action: Unknown format - no action taken"
