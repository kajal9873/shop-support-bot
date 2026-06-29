from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.db_models import Order
from app.models.schemas import OrderStatusResponse

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[OrderStatusResponse])
def list_orders(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return [
        OrderStatusResponse(
            order_id=o.order_id, status=o.status, customer_name=o.customer_name, items=o.items
        )
        for o in orders
    ]


@router.get("/{order_id}", response_model=OrderStatusResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderStatusResponse(
        order_id=order.order_id,
        status=order.status,
        customer_name=order.customer_name,
        items=order.items,
    )