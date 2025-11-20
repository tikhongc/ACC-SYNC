#!/usr/bin/env python3
"""
Refresh authentication token
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def refresh_token():
    """Refresh the authentication token"""
    
    print("Refreshing Authentication Token...")
    print("=" * 50)
    
    try:
        import utils
        
        # Try to refresh token
        print("Attempting to refresh token...")
        
        # Check current token status
        current_token = utils.get_access_token()
        if current_token:
            print(f"Current token length: {len(current_token)}")
        else:
            print("No current token found")
        
        # Force refresh
        refreshed = utils.refresh_access_token()
        
        if refreshed:
            print("SUCCESS: Token refreshed successfully")
            
            # Verify new token
            new_token = utils.get_access_token()
            if new_token:
                print(f"New token length: {len(new_token)}")
                print(f"New token preview: {new_token[:20]}...")
                return True
            else:
                print("ERROR: No token after refresh")
                return False
        else:
            print("ERROR: Token refresh failed")
            return False
            
    except Exception as e:
        print(f"ERROR: Token refresh failed: {e}")
        return False

def check_token_validity():
    """Check if current token is valid"""
    
    print("\nChecking Token Validity...")
    print("=" * 30)
    
    try:
        import utils
        import config
        import requests
        
        token = utils.get_access_token()
        if not token:
            print("No token available")
            return False
        
        # Test token with a simple API call
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        test_url = f"{config.AUTODESK_API_BASE}/userprofile/v1/users/@me"
        response = requests.get(test_url, headers=headers, timeout=10)
        
        print(f"Token test status: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"SUCCESS: Token is valid for user {user_data.get('userName', 'Unknown')}")
            return True
        elif response.status_code == 401:
            print("ERROR: Token is invalid or expired")
            return False
        else:
            print(f"ERROR: Unexpected response: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"ERROR: Token validation failed: {e}")
        return False

if __name__ == "__main__":
    # Check current token
    is_valid = check_token_validity()
    
    if not is_valid:
        print("\nToken is invalid, attempting refresh...")
        success = refresh_token()
        
        if success:
            print("\nRe-checking token after refresh...")
            is_valid = check_token_validity()
            
            if is_valid:
                print("\nSUCCESS: Token is now valid!")
                print("You can proceed with the sync test.")
            else:
                print("\nERROR: Token is still invalid after refresh")
                print("Please re-authenticate via the web interface:")
                print("1. Run: python app.py")
                print("2. Go to: http://localhost:8080")
                print("3. Click 'Login with Autodesk'")
        else:
            print("\nERROR: Token refresh failed")
            print("Please re-authenticate via the web interface")
    else:
        print("\nToken is valid - you can proceed with sync test!")
