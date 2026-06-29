from app.rag.embeddings import embed_text
from app.rag.vector_store import query_collection


def retrieve_relevant_docs(query: str, top_k: int = 3):
    query_embedding = embed_text(query)
    results = query_collection(query_embedding, top_k=top_k)

    docs = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    return [
        {"document": doc, "distance": dist, "metadata": meta}
        for doc, dist, meta in zip(docs, distances, metadatas)
    ]


def seed_faq_into_vector_store(faqs: list):
    """faqs: list of {"question": str, "answer": str, "category": str}"""
    from app.rag.embeddings import embed_batch
    from app.rag.vector_store import add_documents

    questions = [f["question"] for f in faqs]
    embeddings = embed_batch(questions)
    ids = [f"faq-{i}" for i in range(len(faqs))]
    metadatas = [{"answer": f["answer"], "category": f["category"]} for f in faqs]

    add_documents(ids=ids, documents=questions, embeddings=embeddings, metadatas=metadatas)