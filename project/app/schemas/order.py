from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, field_validator
from app.models.models import OrderStatus


class OrderCreate(BaseModel):
    order_date: Optional[datetime] = None
    product_name: str
    category: Optional[str] = None
    quantity: int
    unit_price: Decimal
    status: Optional[OrderStatus] = OrderStatus.pending

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("quantity must be greater than 0")
        return v

    @field_validator("unit_price")
    @classmethod
    def validate_unit_price(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("unit_price must be greater than 0")
        return v


class OrderUpdate(BaseModel):
    order_date: Optional[datetime] = None
    product_name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[Decimal] = None
    status: Optional[OrderStatus] = None

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v <= 0:
            raise ValueError("quantity must be greater than 0")
        return v

    @field_validator("unit_price")
    @classmethod
    def validate_unit_price(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        if v is not None and v <= 0:
            raise ValueError("unit_price must be greater than 0")
        return v


class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    order_date: datetime
    product_name: str
    category: Optional[str]
    quantity: int
    unit_price: Decimal
    total_amount: Decimal
    status: OrderStatus
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


class PaginatedOrders(BaseModel):
    data: list[OrderResponse]
    page: int
    limit: int
    total: int
    total_pages: int