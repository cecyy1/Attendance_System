import requests

URL = "http://127.0.0.1:5000/handle_clock"
EMPLOYEE_ID = 1

data = {
    "employee_id": EMPLOYEE_ID
}

response = requests.post(URL, data=data)

print("Status Code:", response.status_code)
print("Response:", response.text)
