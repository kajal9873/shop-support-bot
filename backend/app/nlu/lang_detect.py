from typing import List, Dict
from app.nlu.codemix_utils import HINDI_WORD_LIST


def detect_language_tokens(text: str) -> List[Dict]:
    """
    Token-level language tagging (heuristic, dictionary-based).
    Returns list of {"token": str, "lang": "hi" | "en" | "other"}.
    """
    tokens = text.split()
    tagged = []

    for tok in tokens:
        clean = "".join(ch for ch in tok.lower() if ch.isalpha())
        if not clean:
            tagged.append({"token": tok, "lang": "other"})
        elif clean in HINDI_WORD_LIST:
            tagged.append({"token": tok, "lang": "hi"})
        else:
            tagged.append({"token": tok, "lang": "en"})

    return tagged


def detect_dominant_language(text: str) -> str:
    tags = detect_language_tokens(text)
    if not tags:
        return "en"
    hi_count = sum(1 for t in tags if t["lang"] == "hi")
    en_count = sum(1 for t in tags if t["lang"] == "en")
    return "hi" if hi_count > en_count else "en"