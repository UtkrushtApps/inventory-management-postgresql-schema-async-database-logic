# Task Overview

StockTrack is a modern inventory management app for small business warehouses. The REST API is complete and exposes endpoints to add products, list all products, and fetch a product by ID. Currently, neither the database schema nor database logic are present. You need to (1) design and implement the PostgreSQL schema (tables for products and anything else required) and (2) complete the async PostgreSQL integration in the code, so products can be reliably stored and retrieved via the API.

## Project Structure & Guidance
- The FastAPI app is fully scaffolded under `/root/task/app`. Routers, Pydantic models, and route logic are present.
- All HTTP endpoints and Pydantic validation are implemented; your job is to create the database schema and fill out async DB logic only.
- Asynchronous DB operations must use `asyncpg` (all endpoints expect non-blocking async DB calls).
- Focus files: `app/database.py` (DB connection + helpers), `app/routes/products.py` (implement async DB logic for routers).
- Don't change routing, middleware, or Pydantic schemas.
- `docker-compose.yml` starts services; `run.sh` runs migrations, sample data, and readiness checks after containers are up.
- Change only SQL files (`schema.sql`, `data/sample_data.sql`) and Python async DB logic in route/database files.

## Database Access
- **Host:** postgres
- **Port:** 5432
- **Database:** stocktrack_db
- **Username:** stocktrack_user
- **Password:** STpass123
- Access via tools like pgAdmin, DBeaver, or psql for data inspection.
- Database is initially empty. You must create all tables and insert data for API testing.
- **Connection string:** `postgresql://stocktrack_user:STpass123@postgres:5432/stocktrack_db`
- All files reside in `/root/task`.

## Objectives
- **PostgreSQL Design:** Design a `products` table including unique IDs, name, description, sku, price, stock count, and created_at timestamp. Use appropriate data types, primary/unique keys, and NOT NULL constraints.
- **Async Logic:** Implement pure async PostgreSQL logic in `database.py` and `routes/products.py` so all product endpoints become functional.
- **Testing:** Add at least 3 sample products in `sample_data.sql` for API testability.
- **Data Integrity:** Prevent duplicate SKUs, ensure non-negative stock counts, and handle error cases for product lookup/addition.
- **Efficiency:** Ensure product retrievals use indexed columns for fast lookup.

## How to Verify
- Use `/products` to list all products and `/products/{id}` to retrieve a product by ID. Confirm insertion via POST `/products` works.
- Check constraints: Adding a duplicate SKU or invalid data should yield error responses.
- Review schema with DB client: verify table, constraints, and actual records.
