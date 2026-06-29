from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func

from app.db.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String, default="general")
    created_at = Column(DateTime, server_default=func.now())


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True, nullable=False)
    customer_name = Column(String, nullable=True)
    status = Column(String, default="placed")  # placed, packed, shipped, delivered, cancelled
    items = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime, server_default=func.now())


class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String, default="general")


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    message = Column(Text)
    reply = Column(Text)
    intent = Column(String, nullable=True)
    detected_language = Column(String, nullable=True)
    cmi_score = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())