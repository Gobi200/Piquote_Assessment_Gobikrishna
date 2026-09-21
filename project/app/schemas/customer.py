from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    city: Optional[str] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    city: Optional[str] = None


class CustomerResponse(BaseModel):
    customer_id: int
    name: str
    email: str
    phone: Optional[str]
    city: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


class PaginatedCustomers(BaseModel):
    data: list[CustomerResponse]
    page: int
    limit: int
    total: int
    total_pages: int