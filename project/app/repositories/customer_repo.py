from typing import Optional
from sqlalchemy.orm import Session
from app.models.models import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


def get_by_id(db: Session, customer_id: int) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()


def get_by_email(db: Session, email: str) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.email == email).first()


def get_all(
    db: Session,
    name: Optional[str],
    email: Optional[str],
    city: Optional[str],
    page: int,
    limit: int,
) -> tuple[list[Customer], int]:
    query = db.query(Customer)
    if name:
        query = query.filter(Customer.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Customer.email.ilike(f"%{email}%"))
    if city:
        query = query.filter(Customer.city.ilike(f"%{city}%"))
    total = query.count()
    customers = query.offset((page - 1) * limit).limit(limit).all()
    return customers, total


def create(db: Session, data: CustomerCreate) -> Customer:
    customer = Customer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def update(db: Session, customer: Customer, data: CustomerUpdate) -> Customer:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)
    db.commit()
    db.refresh(customer)
    return customer


def delete(db: Session, customer: Customer) -> None:
    db.delete(customer)
    db.commit()
