from pydantic import BaseModel, constr, validator
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: constr(min_length=1, max_length=100)
    description: Optional[constr(max_length=255)] = None
    sku: constr(min_length=1, max_length=50)
    price: float
    stock_count: int
    
    @validator('price')
    def price_positive(cls, v):
        if v < 0:
            raise ValueError('price must be non-negative')
        return v
    
    @validator('stock_count')
    def stock_non_negative(cls, v):
        if v < 0:
            raise ValueError('stock_count must be non-negative')
        return v

class Product(ProductCreate):
    id: int
    created_at: datetime
