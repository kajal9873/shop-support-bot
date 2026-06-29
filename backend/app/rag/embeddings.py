from sentence_transformers import SentenceTransformer
from app.config import settings

_model = None


def get_embedding_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def embed_text(text: str):
    model = get_embedding_model()
    return model.encode(text, normalize_embeddings=True).tolist()


def embed_batch(texts: list):
    model = get_embedding_model()
    return model.encode(texts, normalize_embeddings=True).tolist()