SYSTEM_PROMPT = """You are a helpful customer support assistant for a local Indian retail shop.
You respond naturally in Hinglish (Hindi-English mix) matching the customer's language style.
Keep replies short, polite, and direct. Use the provided context (FAQs/order info) to answer accurately.
If you don't know the answer, say so honestly and offer to connect them to the shop owner.
"""


def build_chat_prompt(user_message: str, context_docs: list = None, order_info: dict = None) -> str:
    context_block = ""
    if context_docs:
        context_block = "\n\nRelevant shop info:\n" + "\n".join(
            f"- {d['metadata'].get('answer', d['document'])}" for d in context_docs
        )

    order_block = ""
    if order_info:
        order_block = f"\n\nOrder info: {order_info}"

    return f"{SYSTEM_PROMPT}{context_block}{order_block}\n\nCustomer: {user_message}\nAssistant:"