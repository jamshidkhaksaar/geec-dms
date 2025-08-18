#!/usr/bin/env python3
"""
Production Setup Script for GEEC DMS
Run this script after deploying to shared hosting to verify setup
"""

import os
import sys
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash

def load_env_file():
    """Load environment variables from .env file"""
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key] = value
        return env_vars
    except FileNotFoundError:
        print("Error: .env file not found!")
        return None

def test_database_connection(env_vars):
    """Test database connection"""
    print("Testing database connection...")
    try:
        connection = mysql.connector.connect(
            host=env_vars.get('DB_HOST', 'localhost'),
            database=env_vars.get('DB_NAME'),
            user=env_vars.get('DB_USER'),
            password=env_vars.get('DB_PASSWORD')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            result = cursor.fetchone()
            if result:
                user_count = result[0]
                print(f"✓ Database connection successful! Found {user_count} users.")
            else:
                print("✓ Database connection successful!")
            cursor.close()
            connection.close()
            return True
    except Error as e:
        print(f"✗ Database connection failed: {e}")
        return False

def check_directories():
    """Check if required directories exist and have proper permissions"""
    print("Checking directories...")
    
    required_dirs = ['uploads', 'static', 'templates']
    for directory in required_dirs:
        if os.path.exists(directory):
            if os.access(directory, os.W_OK):
                print(f"✓ {directory}/ exists and is writable")
            else:
                print(f"⚠ {directory}/ exists but may not be writable")
        else:
            print(f"✗ {directory}/ directory missing")
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"✓ Created {directory}/ directory")
            except Exception as e:
                print(f"✗ Failed to create {directory}/: {e}")

def check_required_files():
    """Check if all required files are present"""
    print("Checking required files...")
    
    required_files = [
        'app.py', 'passenger_wsgi.py', '.env', 
        'database_schema.sql', 'requirements.txt'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")

def update_default_passwords(env_vars):
    """Update default user passwords"""
    print("\nWould you like to update default user passwords? (recommended for production)")
    response = input("Update passwords? (y/n): ").strip().lower()
    
    if response != 'y':
        print("Skipping password update.")
        return
    
    try:
        connection = mysql.connector.connect(
            host=env_vars.get('DB_HOST', 'localhost'),
            database=env_vars.get('DB_NAME'),
            user=env_vars.get('DB_USER'),
            password=env_vars.get('DB_PASSWORD')
        )
        
        cursor = connection.cursor()
        
        # Update passwords for default users
        users = ['admin', 'ceo', 'user']
        for username in users:
            print(f"\nSet password for {username}:")
            password = input(f"Enter new password for {username}: ")
            if password:
                password_hash = generate_password_hash(password)
                cursor.execute(
                    "UPDATE users SET password = %s WHERE username = %s",
                    (password_hash, username)
                )
                print(f"✓ Password updated for {username}")
        
        connection.commit()
        cursor.close()
        connection.close()
        print("✓ All passwords updated successfully!")
        
    except Error as e:
        print(f"✗ Failed to update passwords: {e}")

def main():
    """Main setup function"""
    print("GEEC DMS - Production Setup Verification")
    print("=" * 50)
    
    # Load environment variables
    env_vars = load_env_file()
    if not env_vars:
        print("Please create .env file first!")
        return False
    
    print("✓ Environment file loaded")
    
    # Check required files
    check_required_files()
    
    # Check directories
    check_directories()
    
    # Test database connection
    if not test_database_connection(env_vars):
        print("\nPlease fix database connection issues before proceeding.")
        return False
    
    # Optionally update passwords
    update_default_passwords(env_vars)
    
    print("\n" + "=" * 50)
    print("Setup verification complete!")
    print("\nNext steps:")
    print("1. Test your application in a web browser")
    print("2. Try logging in with your credentials")
    print("3. Upload a test PDF file")
    print("4. Configure SendGrid for email notifications")
    print("5. Enable SSL/HTTPS in your hosting control panel")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
    except Exception as e:
        print(f"\nError during setup: {e}") 