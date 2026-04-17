from typing import Dict

CATEGORY_MAP = {
    "food": "Food",
    "travel": "Travel",
    "transport": "Travel",
    "shopping": "Shopping",
    "health": "Health",
    "medical": "Health",
    "entertainment": "Entertainment",
    "utility": "Other",
}


def categorize_receipt(payload: Dict) -> Dict:
    merchant = payload.get("merchant", "").lower()
    category = payload.get("category") or "Other"

    if not category or category == "Other":
        for keyword, value in CATEGORY_MAP.items():
            if keyword in merchant:
                category = value
                break

    payload["category"] = category
    return payload
