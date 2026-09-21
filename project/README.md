# Customer Order & Business Intelligence API

## Project Overview
FastAPI + Neon PostgreSQL REST API covering customer and order management with SQL JOIN reports.

## Technology Stack
- Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2
- PostgreSQL via Neon
- Alembic (migrations)

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env           # fill in your Neon DATABASE_URL
uvicorn app.main:app --reload
```

Tables are created automatically on startup via `Base.metadata.create_all`.  
Alternatively run `scripts/schema.sql` directly against your Neon database.

## Environment Variables (.env.example)
```
DATABASE_URL=postgresql://user:password@host/dbname
OPENROUTER_API_KEY=your_key
```

## API Documentation

### Customers
| Method | URL | Description |
|--------|-----|-------------|
| POST | /customers | Create customer |
| GET | /customers | List customers (pagination + filters) |
| GET | /customers/{id} | Get customer |
| PUT | /customers/{id} | Update customer |
| DELETE | /customers/{id} | Delete customer |

Filters: `?name=john&city=Chennai&page=1&limit=20`

### Orders
| Method | URL | Description |
|--------|-----|-------------|
| POST | /customers/{id}/orders | Create order |
| GET | /customers/{id}/orders | List orders for customer |
| GET | /orders/{id} | Get order |
| PUT | /orders/{id} | Update order |
| DELETE | /orders/{id} | Delete order |

Filters: `?status=pending&category=Electronics&date_from=2024-01-01&date_to=2024-12-31`

### Reports
| Method | URL | Description |
|--------|-----|-------------|
| GET | /reports/customer-orders | INNER JOIN report |
| GET | /reports/customer-summary | LEFT JOIN report |

## Database Design

### Indexes Created
| Index | Column | Reason |
|-------|--------|--------|
| idx_customers_email | customers.email | Unique constraint lookup, login queries |
| idx_customers_name | customers.name | ILIKE name filter |
| idx_customers_city | customers.city | City filter |
| idx_orders_customer_id | orders.customer_id | FK join, fetch customer orders |
| idx_orders_status | orders.status | Filter by order status |
| idx_orders_order_date | orders.order_date | Date-range queries |

## SQL JOIN Explanation

### INNER JOIN — `GET /reports/customer-orders`
Returns only customers who have at least one order. Used here because the report is order-detail level — a row without an order has no meaning in this context.

### LEFT JOIN — `GET /reports/customer-summary`
Returns ALL customers including those with zero orders. An INNER JOIN would silently exclude new customers who haven't ordered yet, giving an incomplete view of the customer base.

## HTTP Status Codes
- 201 Created, 200 OK, 204 No Content
- 400 Bad Request, 404 Not Found, 409 Conflict (duplicate email), 422 Validation Error, 500 DB Error
