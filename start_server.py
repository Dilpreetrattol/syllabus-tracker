#!/usr/bin/env python3
import os
import sys

# Basic test
print("🚀 Script started!")
print(f"Python: {sys.version}")
print(f"Working dir: {os.getcwd()}")

# Get port
port = os.environ.get('PORT', '10000')
print(f"Port: {port}")

# Execute gunicorn directly  
os.system(f"gunicorn wsgi:app --bind 0.0.0.0:{port} --workers 1 --timeout 120")