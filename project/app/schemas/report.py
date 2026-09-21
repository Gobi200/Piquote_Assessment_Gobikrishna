from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class CustomerOrderReport(BaseModel):
    customer_id: int
    customer_name: str
    order_id: int
    product_name: str
    total_amount: Decimal


class CustomerSummaryReport(BaseModel):
    customer_id: int
    customer_name: str
    total_orders: int
    total_amount: Decimal
