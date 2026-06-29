from groq import Groq
from app.config import settings
from app.llm.prompt_templates import build_chat_prompt

_client = None


def get_groq_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=settings.groq_api_key)
    return _client


def generate_reply(user_message: str, context_docs: list = None, order_info: dict = None) -> str:
    client = get_groq_client()
    prompt = build_chat_prompt(user_message, context_docs, order_info)

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.4,
    )

    return response.choices[0].message.content.strip()