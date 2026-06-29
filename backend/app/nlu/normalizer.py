# Common Romanized Hindi spelling variants -> canonical form
SPELLING_VARIANTS = {
    "kitne": "kitna",
    "kya": "kya",
    "kaha": "kahan",
    "kaha hai": "kahan hai",
    "milega": "milega",
    "chahiye": "chahiye",
    "nahi": "nahin",
}


def normalize_text(text: str) -> str:
    """
    Light normalization: lowercase, strip extra whitespace,
    map common Hinglish spelling variants to a canonical form.
    """
    if not text or not text.strip():
        return ""

    cleaned = " ".join(text.lower().strip().split())

    words = cleaned.split()
    normalized_words = [SPELLING_VARIANTS.get(w, w) for w in words]

    return " ".join(normalized_words)