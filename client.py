import requests

BASE_URL = "http://127.0.0.1:8000"

# login
login = requests.post(f"{BASE_URL}/login", json={
    "username": "maswin_fix",
    "password": "123456"
})

token = login.json()["access_token"]

headers = {
    "Authorization": f"Bearer {token}"
}

# simulate sale
sale = requests.post(
    f"{BASE_URL}/sell",
    json={"id": 1, "qty": 2},
    headers=headers
)

print("SALE RESULT:", sale.json())

# check products
products = requests.get(f"{BASE_URL}/products", headers=headers)

print("PRODUCTS:", products.json())