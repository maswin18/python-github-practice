import requests

# Step 1: Login
login_url = "http://127.0.0.1:8000/login"

login_data = {
    "username": "maswin_fix",
    "password": "123456"
}

login_response = requests.post(login_url, json=login_data)

token = login_response.json()["access_token"]

# Step 2: call protected API
url = "http://127.0.0.1:8000/products"

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers)

print(response.json())