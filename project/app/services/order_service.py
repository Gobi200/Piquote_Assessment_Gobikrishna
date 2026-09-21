import math
from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import order_repo, customer_repo
from app.models.models import OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, PaginatedOrders


def create_order(db: Session, customer_id: int, data: OrderCreate) -> OrderResponse:
    customer = customer_repo.get_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return order_repo.create(db, customer_id, data)


def get_order(db: Session, order_id: int) -> OrderResponse:
    order = order_repo.get_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


def list_customer_orders(
    db: Session,
    customer_id: int,
    status: Optional[OrderStatus],
    category: Optional[str],
    date_from: Optional[datetime],
    date_to: Optional[datetime],
    page: int,
    limit: int,
) -> PaginatedOrders:
    customer = customer_repo.get_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    orders, total = order_repo.get_by_customer(
        db, customer_id, status, category, date_from, date_to, page, limit
    )
    return PaginatedOrders(
        data=orders,
        page=page,
        limit=limit,
        total=total,
        total_pages=math.ceil(total / limit) if total else 0,
    )


def update_order(db: Session, order_id: int, data: OrderUpdate) -> OrderResponse:
    order = order_repo.get_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order_repo.update(db, order, data)


def delete_order(db: Session, order_id: int) -> dict:
    order = order_repo.get_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {order_id} does not exist")
    order_repo.delete(db, order)
    return {"message": f"Order {order_id} deleted successfully"}