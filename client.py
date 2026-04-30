import requests
import time
import logging

logging.basicConfig(
    filename="sync.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_URL = "http://127.0.0.1:8000"

# Step 1: Login
login_data = {
    "username": "maswin_fix",
    "password": "123456"
}

def get_token():
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        return response.json().get("access_token")
    except:
        print("Server not available...")
        return None

def sync_job():
    logging.info("Starting sync job")

    token = get_token()

    if not token:
        logging.error("Login failed - no token")
        print("Skipping...")
        return
    
    headers = {
        "Authorization": f"Bearer {token}"
    }

    sync_data = [
        {"id": 1, "name": "Shoes", "qty": 250},
        {"id": 4, "name": "Bag", "qty": 20}
    ]

    logging.info(f"Sending sync data: {sync_data}")

    try:
        sync_response = requests.post(f"{BASE_URL}/sync", json=sync_data, headers=headers)
        logging.info(f"Sync response: {sync_response.json()}")
    except Exception as e:
        logging.error(f"Sync failed: {e}")
        return

    products_response = requests.get(f"{BASE_URL}/products", headers=headers)

    if products_response.status_code == 401:
        logging.warning("Token expired, retrying login")

        token = get_token()
        headers["Authorization"] = f"Bearer {token}"

        products_response = requests.get(f"{BASE_URL}/products", headers=headers)

    logging.info(f"Products after sync: {products_response.json()}")

    print ("Sync OK")

# Run every 10 seconds
try:
    while True:
        print("\n--- Running sync job ---")
        sync_job()
        time.sleep(10)
except:
    print("\nStopped by user.")

