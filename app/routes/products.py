from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.schemas import Product, ProductCreate
from app.database import get_pool

router = APIRouter(prefix="/products")

@router.get("/", response_model=List[Product])
async def list_products():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name, description, sku, price, stock_count, created_at FROM products ORDER BY id ASC;")
        return [Product(**dict(row)) for row in rows]

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, name, description, sku, price, stock_count, created_at FROM products WHERE id = $1;", product_id)
        if not row:
            raise HTTPException(status_code=404, detail="Product not found")
        return Product(**dict(row))

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    pool = await get_pool()
    async with pool.acquire() as conn:
        try:
            row = await conn.fetchrow(
                """
                INSERT INTO products (name, description, sku, price, stock_count)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id, name, description, sku, price, stock_count, created_at
                """,
                product.name, product.description, product.sku, product.price, product.stock_count
            )
            return Product(**dict(row))
        except Exception as e:
            raise HTTPException(status_code=400, detail="Could not create product. Ensure SKU is unique and fields are valid.")
