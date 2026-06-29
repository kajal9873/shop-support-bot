from typing import Optional, List
from pydantic import BaseModel


# ---------- Chat ----------

class ChatRequest(BaseModel):
    message: str
    session_id: str


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    intent: Optional[str] = None
    detected_language: Optional[str] = None
    cmi_score: Optional[float] = None


# ---------- Orders ----------

class OrderStatusResponse(BaseModel):
    order_id: str
    status: str
    customer_name: Optional[str] = None
    items: Optional[str] = None


# ---------- Products / Admin ----------

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int = 0
    category: str = "general"


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category: str

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None