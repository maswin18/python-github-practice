import requests
import threading

BASE_URL = "http://127.0.0.1:8000"

# Login
login = requests.post(f"{BASE_URL}/login", json={
    "username": "maswin_fix",
    "password": "123456"
})

token = login.json()["access_token"]

headers = {
    "Authorization": f"Bearer {token}"
}

def make_sale():
    response = requests.post(
        f"{BASE_URL}/sell",
        json={"id": 10, "qty": 2},
        headers=headers
    )
    print(response.json())

# simulate 2 users at same time
t1 = threading.Thread(target=make_sale)
t2 = threading.Thread(target=make_sale)

t1.start()
t2.start()

t1.join()
t2.join()