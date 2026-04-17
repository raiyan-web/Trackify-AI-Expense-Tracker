import os
import base64
import json
from typing import Any, Dict

try:
    import anthropic
except ImportError:
    anthropic = None

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = os.getenv("CLAUDE_MODEL", "claude-3.5-mini")


def extract_receipt(image_bytes: bytes) -> Dict[str, Any]:
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    prompt = (
        "Extract this receipt and return ONLY JSON with keys merchant, date, total, items, category, raw_text. "
        "If a field is unavailable, return an empty string or empty array."
    )
    if anthropic and ANTHROPIC_API_KEY:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens_to_sample=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_b64,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt,
                        },
                    ],
                }
            ],
        )
        text = response.content[0].text
        try:
            payload = json.loads(text)
        except Exception:
            payload = {
                "merchant": "",
                "date": "",
                "total": 0.0,
                "items": [],
                "category": "Other",
                "raw_text": text,
            }
        return payload

    # Fallback stub if Anthropics is not installed or API key missing
    return {
        "merchant": "Unknown Merchant",
        "date": "2025-01-01",
        "total": 0.0,
        "items": [],
        "category": "Other",
        "raw_text": "AI extraction unavailable. Set ANTHROPIC_API_KEY to enable Claude.",
    }
