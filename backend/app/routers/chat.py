from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.schemas import ChatRequest, ChatResponse
from app.models.db_models import ChatLog
from app.nlu.codemix_utils import compute_cmi
from app.nlu.lang_detect import detect_dominant_language
from app.nlu.intent_classifier import classify_intent
from app.rag.retriever import retrieve_relevant_docs
from app.llm.groq_client import generate_reply

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    cmi_score = compute_cmi(req.message)
    detected_lang = detect_dominant_language(req.message)
    intent_result = classify_intent(req.message)

    context_docs = retrieve_relevant_docs(req.message, top_k=3)

    try:
        reply = generate_reply(req.message, context_docs=context_docs)
    except Exception as e:
        print(f"GROQ ERROR: {type(e).__name__}: {e}")
        reply = "Sorry, abhi main jawab nahi de paa raha. Thodi der mein try karo."

    log = ChatLog(
        session_id=req.session_id,
        message=req.message,
        reply=reply,
        intent=intent_result["intent"],
        detected_language=detected_lang,
        cmi_score=cmi_score,
    )
    db.add(log)
    db.commit()

    return ChatResponse(
        reply=reply,
        session_id=req.session_id,
        intent=intent_result["intent"],
        detected_language=detected_lang,
        cmi_score=cmi_score,
    )