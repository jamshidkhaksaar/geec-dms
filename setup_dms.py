#!/usr/bin/env python3
"""
GEEC Online DMS Setup Script
"""

import os
import sys
import subprocess

def main():
    print("GEEC Online DMS Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("Error: Python 3.7+ required")
        sys.exit(1)
    
    print("✅ Python version OK")
    
    # Install dependencies
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed")
    except:
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create directories
    directories = ['uploads', 'static/images', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directories created")
    
    # Create .env file
    env_content = """# GEEC DMS Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=geec_dms
SECRET_KEY=change-this-in-production
FLASK_ENV=development
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ Configuration file created")
    
    print("\nSetup complete!")
    print("Next steps:")
    print("1. Set up MySQL database using database_schema.sql")
    print("2. Update .env with your database credentials")
    print("3. Run: python app.py")

if __name__ == "__main__":
    main() 