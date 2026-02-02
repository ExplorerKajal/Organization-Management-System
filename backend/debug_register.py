import requests
try:
    resp = requests.post("http://127.0.0.1:5000/auth/register", json={
        "username": "debuguser",
        "email": "debug@example.com",
        "password": "pass",
        "role": "Employee"
    })
    print(f"Status: {resp.status_code}")
    with open("error_page.html", "w", encoding="utf-8") as f:
        f.write(resp.text)
    print("Wrote error_page.html")
except Exception as e:
    print(f"Error: {e}")
