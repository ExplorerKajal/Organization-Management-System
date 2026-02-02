import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_auth():
    print("Testing Authentication Module...")
    
    # 1. Register a new user
    print("\n[1] Testing Registration...")
    reg_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "role": "Employee"
    }
    
    # Clean up potentially existing user first (simple hack for this test using a manual check if we had a delete endpoint, but here we just try register and expect success or already exists)
    # Ideally, we would drop DB or use a fresh test DB. For this quick check, we'll handle 400 'already exists' gracefully.

    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=reg_data)
        if response.status_code == 201:
            print("Registration Successful")
        elif response.status_code == 400 and "already exists" in response.text:
             print("User already exists (Expected if re-running)")
        else:
             print(f"Registration Failed: {response.status_code} - {response.text[:200]}")
    except Exception as e:
        print(f"Registration Request Failed: {e}")
        return

    # 2. Login
    print("\n[2] Testing Login...")
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    token = None
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            role = response.json().get("user", {}).get("role")
            if token and role == "Employee":
                print(f"Login Successful. Token received. Role: {role}")
            else:
                print(f"Login Successful but missing token or incorrect role. Response: {response.json()}")
        else:
            print(f"Login Failed: {response.status_code} - {response.text[:200]}")
    except Exception as e:
        print(f"Login Request Failed: {e}")

    # 3. Login with wrong password
    print("\n[3] Testing Invalid Login...")
    bad_login_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=bad_login_data)
        if response.status_code == 401:
             print("Invalid Login Correctly Rejected")
        else:
             print(f"Invalid Login TEST FAILED: {response.status_code} - {response.text[:200]}")
    except Exception as e:
        print(f"Invalid Login Request Failed: {e}")

    # 4. Test Protected Route
    print("\n[4] Testing Protected Route (/auth/me)...")
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            if response.status_code == 200:
                user_info = response.json()
                if user_info.get("username") == "testuser":
                     print("Protected Route Access Successful. User verified.")
                else:
                     print(f"Protected Route Access Failed: Username mismatch. Got {user_info}")
            else:
                 print(f"Protected Route Access Failed: {response.status_code} - {response.text[:200]}")
        except Exception as e:
            print(f"Protected Route Request Failed: {e}")
    else:
        print("Skipping Protected Route Test due to missing token.")

if __name__ == "__main__":
    test_auth()
