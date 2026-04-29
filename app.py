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