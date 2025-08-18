#!/usr/bin/env python3
"""
WSGI configuration for GEEC DMS Flask application
This file is required for Namecheap shared hosting
"""

import sys
import os

# Add your project directory to the sys.path
sys.path.insert(0, os.path.dirname(__file__))

from app import app as application

if __name__ == "__main__":
    application.run() 