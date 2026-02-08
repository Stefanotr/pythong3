"""
Setup script to initialize admin account for testing.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Game', 'src'))

from Utils.UserManager import UserManager

def setup_admin():
    """Setup admin account."""
    print("Setting up admin account...")
    
    try:
        user_manager = UserManager()
        
        # Check if admin already exists
        if user_manager.user_exists("admin"):
            print("✓ Admin account already exists")
            return True
        
        # Create admin account with password "admin"
        success = user_manager.register_user("admin", "admin")
        
        if success:
            print("✓ Admin account created successfully")
            print("  Username: admin")
            print("  Password: admin")
            print("\nAdmin features:")
            print("  - Touches 1-8: Jump to stages")
            print("  - Touche P: Add 1000 currency")
            return True
        else:
            print("✗ Failed to create admin account")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    setup_admin()
