import requests

url = "http://127.0.0.1:8000/products"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYXN3aW5fZml4IiwiZXhwIjoxNzc3NTAyNjM0fQ.A4fA9JWoBqc03grpMyg8Uc2kbS1ZtO2e33snfQQ8ssw"

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers)

print(response.json())