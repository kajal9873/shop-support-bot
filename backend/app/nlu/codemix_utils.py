import re

HINDI_WORD_LIST = {
    "hai", "kya", "kaha", "kaise", "kab", "kyu", "kyun", "mera", "mujhe", "tum",
    "aap", "bhai", "abhi", "nahi", "haan", "chahiye", "batao", "order", "kitna",
    "kitne", "milega", "available", "hua", "tak", "jayega", "aayega", "khulta",
    "namaste", "shubh", "prabhat", "dijiye", "karo", "karna",
}


def detect_script_mix(cmi: float) -> str:
    if cmi < 0.05:
        return "pure_en"
    elif cmi > 0.85:
        return "pure_hi"
    elif cmi < 0.3:
        return "light_mix"
    else:
        return "heavy_mix"


def compute_cmi(text: str) -> float:
    """
    Simple Code-Mix Index: ratio of Hindi(Romanized)-flagged tokens
    to total tokens. Range [0.0, 1.0].
    """
    if not text or not text.strip():
        return 0.0

    tokens = re.findall(r"[a-zA-Z]+", text.lower())
    if not tokens:
        return 0.0

    hindi_count = sum(1 for t in tokens if t in HINDI_WORD_LIST)
    return round(hindi_count / len(tokens), 3)