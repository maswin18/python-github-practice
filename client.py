import requests
import time

BASE_URL = "http://127.0.0.1:8000"

# Step 1: Login
login_data = {
    "username": "maswin_fix",
    "password": "123456"
}

def get_token():
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    return response.json().get("access_token")

def sync_job():
    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    sync_data = [
        {"id": 1, "name": "Shoes", "qty": 250},
        {"id": 4, "name": "Bag", "qty": 20}
    ]

    sync_response = requests.post(f"{BASE_URL}/sync", json=sync_data, headers=headers)

    print("Sync:", sync_response.json())

    products_response = requests.get(f"{BASE_URL}/products", headers=headers)

    if products_response.status_code == 401:
        print("Token expired, retrying...")
        token = get_token()
        headers["Authorization"] = f"Bearer {token}"
        products_response = requests.get(f"{BASE_URL}/products", headers=headers)

    print("Products:", products_response.json())

# Run every 10 seconds
while True:
    print("\n--- Running sync job ---")
    sync_job()
    time.sleep(10)