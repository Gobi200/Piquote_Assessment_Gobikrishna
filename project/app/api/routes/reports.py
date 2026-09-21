from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.repositories import report_repo
from app.schemas.report import CustomerOrderReport, CustomerSummaryReport

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/customer-orders", response_model=list[CustomerOrderReport])
def customer_orders_report(db: Session = Depends(get_db)):
    return report_repo.get_customer_orders(db)


@router.get("/customer-summary", response_model=list[CustomerSummaryReport])
def customer_summary_report(db: Session = Depends(get_db)):
    return report_repo.get_customer_summary(db)
