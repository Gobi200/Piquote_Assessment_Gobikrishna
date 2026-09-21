import math
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import customer_repo
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse, PaginatedCustomers


def create_customer(db: Session, data: CustomerCreate) -> CustomerResponse:
    if customer_repo.get_by_email(db, data.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return customer_repo.create(db, data)


def get_customer(db: Session, customer_id: int) -> CustomerResponse:
    customer = customer_repo.get_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


def list_customers(
    db: Session,
    name: Optional[str],
    email: Optional[str],
    city: Optional[str],
    page: int,
    limit: int,
) -> PaginatedCustomers:
    customers, total = customer_repo.get_all(db, name, email, city, page, limit)
    return PaginatedCustomers(
        data=customers,
        page=page,
        limit=limit,
        total=total,
        total_pages=math.ceil(total / limit) if total else 0,
    )


def update_customer(db: Session, customer_id: int, data: CustomerUpdate) -> CustomerResponse:
    customer = customer_repo.get_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    if data.email and data.email != customer.email:
        if customer_repo.get_by_email(db, data.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return customer_repo.update(db, customer, data)


def delete_customer(db: Session, customer_id: int) -> dict:
    customer = customer_repo.get_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with id {customer_id} does not exist")
    customer_repo.delete(db, customer)
    return {"message": f"Customer {customer_id} deleted successfully"}