import re
from typing import List, Dict

QUANTITY_UNITS = ["kg", "g", "ltr", "l", "packet", "packets", "piece", "pieces"]


def extract_entities(text: str) -> List[Dict]:
    entities = []

    # Order ID: #ORD1234 or ORD1234
    for match in re.finditer(r"#?(ORD\d+)", text, re.IGNORECASE):
        entities.append({"text": match.group(0), "label": "ORDER_ID"})

    # Quantity: number + unit
    for match in re.finditer(
        r"(\d+\.?\d*)\s*(" + "|".join(QUANTITY_UNITS) + r")\b", text, re.IGNORECASE
    ):
        entities.append({"text": match.group(0), "label": "QUANTITY"})

    # Product: naive noun-after-quantity heuristic
    for match in re.finditer(
        r"(?:\d+\.?\d*\s*(?:" + "|".join(QUANTITY_UNITS) + r")\s+)([a-zA-Z]+)", text, re.IGNORECASE
    ):
        entities.append({"text": match.group(1), "label": "PRODUCT"})

    return entities