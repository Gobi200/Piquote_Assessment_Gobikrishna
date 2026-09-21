from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.api.routes import customers, orders, reports, ai
from app.database.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Order & Business Intelligence API")

app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(reports.router)
app.include_router(ai.router)


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(status_code=500, content={"detail": "A database error occurred"})
