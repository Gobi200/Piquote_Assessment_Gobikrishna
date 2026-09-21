from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Customer, Order
from app.schemas.report import CustomerOrderReport, CustomerSummaryReport


def get_customer_orders(db: Session) -> list[CustomerOrderReport]:
    rows = (
        db.query(
            Customer.customer_id.label("customer_id"),
            Customer.name.label("customer_name"),
            Order.order_id.label("order_id"),
            Order.product_name,
            Order.total_amount,
        )
        .join(Order, Customer.customer_id == Order.customer_id)
        .all()
    )
    return [CustomerOrderReport(**row._asdict()) for row in rows]


def get_customer_summary(db: Session) -> list[CustomerSummaryReport]:
    rows = (
        db.query(
            Customer.customer_id.label("customer_id"),
            Customer.name.label("customer_name"),
            func.count(Order.order_id).label("total_orders"),
            func.coalesce(func.sum(Order.total_amount), 0).label("total_amount"),
        )
        .outerjoin(Order, Customer.customer_id == Order.customer_id)
        .group_by(Customer.customer_id, Customer.name)
        .all()
    )
    return [CustomerSummaryReport(**row._asdict()) for row in rows]
