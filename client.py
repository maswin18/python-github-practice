import requests

# Step 1: Login
login_url = "http://127.0.0.1:8000/login"

login_data = {
    "username": "maswin_fix",
    "password": "123456"
}

login_response = requests.post(login_url, json=login_data)

if login_response.status_code != 200:
    print("Login failed:", login_response.text)
    exit()

token = login_response.json().get("access_token")

if not token:
    print("No token received")
    exit()

# Step 2: call API
url = "http://127.0.0.1:8000/products"

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Products:", response.json())
else:
    print("API error:", response.status_code, response.text)