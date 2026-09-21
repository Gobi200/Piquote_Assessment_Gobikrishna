from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, PaginatedOrders
from app.services import order_service

router = APIRouter(tags=["Orders"])


@router.post("/customers/{customer_id}/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(customer_id: int, data: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db, customer_id, data)


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return order_service.get_order(db, order_id)


@router.get("/customers/{customer_id}/orders", response_model=PaginatedOrders)
def list_customer_orders(
    customer_id: int,
    status: Optional[OrderStatus] = None,
    category: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return order_service.list_customer_orders(
        db, customer_id, status, category, date_from, date_to, page, limit
    )


@router.put("/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, data: OrderUpdate, db: Session = Depends(get_db)):
    return order_service.update_order(db, order_id, data)


@router.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return order_service.delete_order(db, order_id)
