#!/usr/bin/env python3
"""
Password Generation Script for GEEC DMS
Use this script to generate secure password hashes for production deployment
"""

from werkzeug.security import generate_password_hash
import getpass

def generate_secure_password():
    """Generate a secure password hash"""
    print("GEEC DMS - Password Hash Generator")
    print("=" * 40)
    
    while True:
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty!")
            continue
        break
    
    while True:
        password = getpass.getpass("Enter password: ")
        confirm_password = getpass.getpass("Confirm password: ")
        
        if password != confirm_password:
            print("Passwords don't match! Please try again.")
            continue
        
        if len(password) < 8:
            print("Password must be at least 8 characters long!")
            continue
        
        break
    
    # Generate hash
    password_hash = generate_password_hash(password)
    
    print(f"\nGenerated hash for user '{username}':")
    print("-" * 50)
    print(password_hash)
    print("-" * 50)
    
    print(f"\nSQL Update Command:")
    print(f"UPDATE users SET password = '{password_hash}' WHERE username = '{username}';")
    print("\nCopy the hash above and use it in your database update.")

if __name__ == "__main__":
    try:
        generate_secure_password()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
    except Exception as e:
        print(f"\nError: {e}") 