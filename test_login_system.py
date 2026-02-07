"""
Test script for the login system.
Tests UserManager, LoginModel, and basic authentication flow.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Utils.UserManager import UserManager
from Models.LoginModel import LoginModel

def test_user_manager():
    """Test UserManager functionality."""
    print("Testing UserManager...")
    
    try:
        # Initialize UserManager
        user_manager = UserManager()
        
        # Test 1: Register a new user
        print("  Test 1: Registering user 'testuser'...")
        success = user_manager.register_user("testuser", "password123")
        assert success, "Registration failed"
        print("    ✓ Registration successful")
        
        # Test 2: Check user exists
        print("  Test 2: Checking if user exists...")
        exists = user_manager.user_exists("testuser")
        assert exists, "User should exist"
        print("    ✓ User exists")
        
        # Test 3: Authenticate user with correct password
        print("  Test 3: Authenticating with correct password...")
        authenticated = user_manager.authenticate_user("testuser", "password123")
        assert authenticated, "Authentication failed"
        print("    ✓ Authentication successful")
        
        # Test 4: Authenticate user with wrong password
        print("  Test 4: Authenticating with wrong password...")
        wrong_auth = user_manager.authenticate_user("testuser", "wrongpassword")
        assert not wrong_auth, "Authentication should fail with wrong password"
        print("    ✓ Authentication correctly failed")
        
        # Test 5: Load and save progression
        print("  Test 5: Testing progression save/load...")
        progression_data = {
            "username": "testuser",
            "current_stage": 2,
            "level": 5,
            "hp": 80,
            "max_hp": 100,
            "damage": 12,
            "drunkenness": 30,
            "coma_risk": 15,
            "position": {"x": 100, "y": 150},
            "inventory": [],
            "completed_acts": [1],
            "completed_rhythms": [1]
        }
        
        saved = user_manager.save_progression("testuser", progression_data)
        assert saved, "Save progression failed"
        print("    ✓ Progression saved")
        
        loaded = user_manager.load_progression("testuser")
        assert loaded is not None, "Load progression failed"
        assert loaded["current_stage"] == 2, "Stage mismatch"
        assert loaded["level"] == 5, "Level mismatch"
        print("    ✓ Progression loaded correctly")
        
        # Cleanup
        print("  Cleanup: Deleting test user...")
        deleted = user_manager.delete_user("testuser")
        assert deleted, "Deletion failed"
        print("    ✓ User deleted")
        
        print("\n✓ All UserManager tests passed!")
        return True
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_login_model():
    """Test LoginModel functionality."""
    print("\nTesting LoginModel...")
    
    try:
        # Initialize LoginModel
        login_model = LoginModel()
        
        # Test 1: Register a user
        print("  Test 1: Registering user 'modeltest'...")
        success = login_model.register("modeltest", "pass456", "pass456")
        assert success, "Registration failed"
        print("    ✓ Registration successful")
        
        # Test 2: Login with correct credentials
        print("  Test 2: Logging in with correct credentials...")
        logged_in = login_model.login("modeltest", "pass456")
        assert logged_in, "Login failed"
        assert login_model.current_user == "modeltest", "Current user not set"
        print("    ✓ Login successful")
        
        # Test 3: Get user progression
        print("  Test 3: Getting user progression...")
        progression = login_model.get_user_progression()
        assert progression is not None, "Progression is None"
        print("    ✓ Progression retrieved")
        
        # Test 4: Save progression
        print("  Test 4: Saving progression...")
        progression["level"] = 10
        saved = login_model.save_user_progression(progression)
        assert saved, "Save failed"
        print("    ✓ Progression saved")
        
        # Test 5: Logout
        print("  Test 5: Logging out...")
        login_model.logout()
        assert login_model.current_user is None, "Current user should be None"
        print("    ✓ Logout successful")
        
        # Cleanup
        print("  Cleanup: Deleting test user...")
        user_manager = UserManager()
        user_manager.delete_user("modeltest")
        print("    ✓ User deleted")
        
        print("\n✓ All LoginModel tests passed!")
        return True
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("LOGIN SYSTEM TEST SUITE")
    print("=" * 60)
    
    results = []
    results.append(test_user_manager())
    results.append(test_login_model())
    
    print("\n" + "=" * 60)
    if all(results):
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("=" * 60)
