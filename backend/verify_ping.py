import requests
try:
    print("Pinging root...")
    r = requests.get("http://127.0.0.1:5000/")
    print(f"Status: {r.status_code}")
    print(f"Text: {r.text}")
except Exception as e:
    print(f"Error: {e}")
