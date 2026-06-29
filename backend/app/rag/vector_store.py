import chromadb
from app.config import settings

_client = None
_collection = None


def get_chroma_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
    return _client


def get_collection():
    global _collection
    if _collection is None:
        client = get_chroma_client()
        _collection = client.get_or_create_collection(name=settings.chroma_collection_name)
    return _collection


def add_documents(ids: list, documents: list, embeddings: list, metadatas: list = None):
    collection = get_collection()
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas or [{} for _ in ids],
    )


def query_collection(query_embedding: list, top_k: int = 3):
    collection = get_collection()
    return collection.query(query_embeddings=[query_embedding], n_results=top_k)