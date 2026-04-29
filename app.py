from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello Maswin, this is your first API!"}

@app.get("/products")
def get_products():
    return [
        {"id": 1, "name": "Shoes", "qty": 100},
        {"id": 2, "name": "T-Shirt", "qty": 50}
    ]

from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    qty: int

Products = [
    {"id": 1, "name": "Shoes", "qty": 100},
    {"id": 2, "name": "T-Shirt", "qty": 50}
]

@app.post("/products")
def add_product(product: Product):
    Products.append(product.dict())
    return {"message": "Product added", "data": product}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for p in Products:
        if p["id"] == product_id:
            Products.remove(p)
            return {"message": "Product deleted"}
    return {"message": "Product not found"}

