from fastapi import FastAPI
from app.routes import products

app = FastAPI(title="StockTrack Inventory API")
app.include_router(products.router)