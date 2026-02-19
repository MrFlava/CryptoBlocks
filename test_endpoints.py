"""
Test script for the crypto API endpoints
Run this to test the endpoints after starting the FastAPI server
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_endpoints():
    print("Testing Crypto API Endpoints")
    print("=" * 50)
    
    # Test 1: Create account (public registration)
    print("\n1. Testing public account creation...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=register_data)
        if response.status_code == 200:
            print("Account created successfully:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Account creation failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error creating account: {e}")
    
    # Test 2: Create account (admin)
    print("\n2. Testing admin account creation...")
    admin_register_data = {
        "username": "adminuser",
        "email": "admin@example.com", 
        "password": "adminpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/accounts", json=admin_register_data)
        if response.status_code == 200:
            print("Admin account created successfully:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Admin account creation failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error creating admin account: {e}")
    
    # Test 3: Login
    print("\n3. Testing login...")
    login_data = {
        "username": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL.replace('/api/v1', '')}/auth/login",
            data=login_data
        )
        if response.status_code == 200:
            token_data = response.json()
            print("Login successful:")
            print(json.dumps(token_data, indent=2))
            access_token = token_data.get("access_token")
        else:
            print(f"Login failed: {response.status_code}")
            print(response.text)
            access_token = None
    except Exception as e:
        print(f"Error logging in: {e}")
        access_token = None
    
    # Test 4: Get currencies
    print("\n4. Testing get currencies...")
    headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}
    
    try:
        response = requests.get(f"{BASE_URL}/currencies", headers=headers)
        if response.status_code == 200:
            print("Currencies retrieved:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to get currencies: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error getting currencies: {e}")
    
    # Test 5: Get providers
    print("\n5. Testing get providers...")
    
    try:
        response = requests.get(f"{BASE_URL}/providers", headers=headers)
        if response.status_code == 200:
            print("Providers retrieved:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to get providers: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error getting providers: {e}")
    
    # Test 6: Get blocks
    print("\n6. Testing get blocks...")
    
    try:
        response = requests.get(f"{BASE_URL}/blocks", headers=headers)
        if response.status_code == 200:
            print("Blocks retrieved:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to get blocks: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error getting blocks: {e}")
    
    print("\n" + "=" * 50)
    print("Testing completed!")

if __name__ == "__main__":
    test_endpoints()
