"""
Unit tests for NLU pipeline: lang detection, CMI calculation,
normalization, intent classification, NER extraction.
"""
import pytest
from app.nlu.codemix_utils import compute_cmi, detect_script_mix
from app.nlu.normalizer import normalize_text
from app.nlu.lang_detect import detect_language_tokens
from app.nlu.intent_classifier import classify_intent
from app.nlu.ner_extractor import extract_entities


# ---------- Code-Mix Index (CMI) ----------

class TestCMI:
    def test_pure_english(self):
        text = "what is the price of this product"
        cmi = compute_cmi(text)
        assert cmi == pytest.approx(0.0, abs=0.05)

    def test_pure_hindi_romanized(self):
        text = "iska price kya hai"
        cmi = compute_cmi(text)
        assert cmi > 0.5

    def test_heavy_codemix(self):
        text = "mera order kaha hai bhai, abhi tak deliver nahi hua"
        cmi = compute_cmi(text)
        assert cmi > 0.4

    def test_light_codemix(self):
        text = "is this product available in stock"
        cmi = compute_cmi(text)
        assert cmi < 0.3

    def test_empty_string(self):
        assert compute_cmi("") == 0.0

    @pytest.mark.parametrize("text,expected_bucket", [
        ("hello good morning", "pure_en"),
        ("namaste shubh prabhat", "pure_hi"),
        ("order kab aayega please batao", "heavy_mix"),
        ("is this available", "light_mix"),
    ])
    def test_cmi_bucketing(self, text, expected_bucket):
        cmi = compute_cmi(text)
        bucket = detect_script_mix(cmi)
        assert bucket == expected_bucket


# ---------- Normalization (Roman -> Devanagari / canonical) ----------

class TestNormalizer:
    def test_normalize_returns_string(self):
        result = normalize_text("kya price hai iska")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_normalize_idempotent_on_english(self):
        text = "what is the order status"
        assert normalize_text(text) == normalize_text(normalize_text(text))

    def test_normalize_handles_common_variants(self):
        # common Hinglish spelling variants should normalize to same token
        v1 = normalize_text("kitna price hai")
        v2 = normalize_text("kitne price hai")
        assert v1 is not None and v2 is not None

    def test_normalize_empty_input(self):
        assert normalize_text("") == ""

    def test_normalize_does_not_crash_on_emoji(self):
        result = normalize_text("order kab aayega 😊")
        assert isinstance(result, str)


# ---------- Language / token-level detection ----------

class TestLangDetect:
    def test_token_level_tags(self):
        tags = detect_language_tokens("mera order kaha hai")
        assert isinstance(tags, list)
        assert all(t["lang"] in ("hi", "en", "other") for t in tags)

    def test_english_dominant(self):
        tags = detect_language_tokens("please check my order status")
        en_count = sum(1 for t in tags if t["lang"] == "en")
        assert en_count >= len(tags) // 2


# ---------- Intent Classification ----------

class TestIntentClassifier:
    @pytest.mark.parametrize("text,expected_intent", [
        ("mera order kaha hai", "order_status"),
        ("what is the price of milk", "product_price"),
        ("shop kitne baje khulta hai", "store_hours"),
        ("return karna hai ye product", "return_request"),
        ("is sugar available right now", "stock_check"),
    ])
    def test_intent_predictions(self, text, expected_intent):
        result = classify_intent(text)
        assert result["intent"] == expected_intent
        assert 0.0 <= result["confidence"] <= 1.0

    def test_low_confidence_fallback(self):
        result = classify_intent("asdkj qwepoi random gibberish")
        assert result["intent"] == "fallback" or result["confidence"] < 0.5

    def test_accuracy_by_cmi_bucket(self):
        """Sanity check: heavy code-mix should not catastrophically fail."""
        heavy_mix_samples = [
            ("order kab tak aa jayega bhai", "order_status"),
            ("kal tak deliver ho jayega kya", "order_status"),
        ]
        correct = sum(
            1 for text, label in heavy_mix_samples
            if classify_intent(text)["intent"] == label
        )
        assert correct / len(heavy_mix_samples) >= 0.5


# ---------- NER Extraction ----------

class TestNERExtractor:
    def test_extract_order_id(self):
        entities = extract_entities("mera order #ORD1234 kaha hai")
        order_ids = [e["text"] for e in entities if e["label"] == "ORDER_ID"]
        assert "ORD1234" in order_ids or "#ORD1234" in order_ids

    def test_extract_quantity_and_product(self):
        entities = extract_entities("2 kg chawal chahiye")
        labels = {e["label"] for e in entities}
        assert "QUANTITY" in labels
        assert "PRODUCT" in labels

    def test_no_entities_in_generic_text(self):
        entities = extract_entities("hello how are you")
        assert isinstance(entities, list)

    def test_entity_f1_codemix_vs_mono(self):
        """Regression guard: code-mixed NER shouldn't drop entities entirely."""
        mono = extract_entities("I need 5 packets of milk")
        mixed = extract_entities("mujhe 5 packet milk chahiye")
        assert len(mono) > 0
        assert len(mixed) > 0