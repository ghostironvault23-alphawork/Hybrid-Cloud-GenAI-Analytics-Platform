import re
from typing import Any, Dict


EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
PHONE_RE = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\d{10})\b")
CARD_RE = re.compile(r"\b(?:\d[ -]*?){13,16}\b")

SENSITIVE_KEYS = {
    "password",
    "secret",
    "token",
    "api_key",
    "apikey",
    "authorization",
    "credit_card",
    "card_number",
}


def mask_text(value: str) -> str:
    value = EMAIL_RE.sub("[MASKED_EMAIL]", value)
    value = PHONE_RE.sub("[MASKED_PHONE]", value)
    value = CARD_RE.sub("[MASKED_CARD]", value)
    return value


def mask_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    masked: Dict[str, Any] = {}
    for key, value in data.items():
        key_lower = key.lower()
        if key_lower in SENSITIVE_KEYS:
            masked[key] = "[MASKED_SECRET]"
        elif isinstance(value, str):
            masked[key] = mask_text(value)
        elif isinstance(value, dict):
            masked[key] = mask_dict(value)
        else:
            masked[key] = value
    return masked
