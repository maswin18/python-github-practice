import requests

BASE_URL = "http://127.0.0.1:8000"

# Step 1: Login
login_data = {
    "username": "maswin_fix",
    "password": "123456"
}

login_response = requests.post(f"{BASE_URL}/login", json=login_data)

if login_response.status_code != 200:
    print("Login failed:", login_response.text)
    exit()

token = login_response.json().get("access_token")

headers = {
    "Authorization": f"Bearer{token}"
}

# Step 2: Sync data (simulate external system)
sync_data = [
    {"id": 1, "name": "Shoes", "qty": 200},
    {"id": 3, "name": "Jacket", "qty": 50}
]

sync_response = requests.post(f"{BASE_URL}/sync", json=sync_data, headers=headers)

print("Sync result:", sync_response.json())

# Step 3: Verify
products_response = requests.get(f"{BASE_URL}/products", headers=headers)

if products_response.status_code == 401:
    print("Token expired, logging in again...")

    login_response = requests.post(f"{BASE_URL}/login", json=login_data)
    token = login_response.json().get("access_token")

    headers = {"Authorization": f"Bearer {token}"}

    products_response = requests.get(f"{BASE_URL}/products", headers=headers)

print("Products:", products_response.json())