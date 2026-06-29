from typing import Dict
from app.nlu.normalizer import normalize_text

# Keyword-based intent rules (swap with fine-tuned model later)
INTENT_KEYWORDS = {
    "order_status": ["order", "kaha hai", "kab aayega", "deliver", "delivery status", "track"],
    "product_price": ["price", "kitna", "cost", "kitne ka", "rate"],
    "store_hours": ["timing", "khulta", "band", "open", "close", "kab khulta"],
    "return_request": ["return", "wapas", "refund", "exchange"],
    "stock_check": ["available", "stock", "milega", "hai kya"],
}


def classify_intent(text: str) -> Dict:
    normalized = normalize_text(text)

    best_intent = "fallback"
    best_score = 0

    for intent, keywords in INTENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in normalized)
        if score > best_score:
            best_score = score
            best_intent = intent

    confidence = min(0.5 + 0.15 * best_score, 0.95) if best_score > 0 else 0.3

    return {"intent": best_intent, "confidence": round(confidence, 2)}