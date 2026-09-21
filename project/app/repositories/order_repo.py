from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from app.models.models import Order, OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate


def get_by_id(db: Session, order_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.order_id == order_id).first()


def get_by_customer(
    db: Session,
    customer_id: int,
    status: Optional[OrderStatus],
    category: Optional[str],
    date_from: Optional[datetime],
    date_to: Optional[datetime],
    page: int,
    limit: int,
) -> tuple[list[Order], int]:
    query = db.query(Order).filter(Order.customer_id == customer_id)
    if status:
        query = query.filter(Order.status == status)
    if category:
        query = query.filter(Order.category.ilike(f"%{category}%"))
    if date_from:
        query = query.filter(Order.order_date >= date_from)
    if date_to:
        query = query.filter(Order.order_date <= date_to)
    total = query.count()
    orders = query.offset((page - 1) * limit).limit(limit).all()
    return orders, total


def create(db: Session, customer_id: int, data: OrderCreate) -> Order:
    total = Decimal(str(data.quantity)) * data.unit_price
    order = Order(
        customer_id=customer_id,
        order_date=data.order_date or datetime.utcnow(),
        product_name=data.product_name,
        category=data.category,
        quantity=data.quantity,
        unit_price=data.unit_price,
        total_amount=total,
        status=data.status,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def update(db: Session, order: Order, data: OrderUpdate) -> Order:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(order, field, value)
    if data.quantity is not None or data.unit_price is not None:
        order.total_amount = Decimal(str(order.quantity)) * order.unit_price
    db.commit()
    db.refresh(order)
    return order


def delete(db: Session, order: Order) -> None:
    db.delete(order)
    db.commit()
