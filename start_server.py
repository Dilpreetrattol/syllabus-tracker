#!/usr/bin/env python3
"""
Production startup script for Render deployment
"""
import os
import sys
import subprocess

def main():
    """Start the application with proper gunicorn configuration"""
    port = os.environ.get('PORT', '10000')
    
    # Debug: Check if app.py exists and can be imported
    try:
        import app
        print(f"✅ Successfully imported app module")
        print(f"✅ App instance found: {hasattr(app, 'app')}")
        if hasattr(app, 'app'):
            print(f"✅ App type: {type(app.app)}")
    except ImportError as e:
        print(f"❌ Failed to import app: {e}")
        return
    
    # Build the correct gunicorn command
    cmd = [
        'gunicorn',
        'app:app',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '1',
        '--timeout', '120',
        '--max-requests', '1000',
        '--preload'
    ]
    
    print(f"Starting server on port {port}")
    print(f"Command: {' '.join(cmd)}")
    
    # Execute gunicorn
    os.execvp('gunicorn', cmd)

if __name__ == '__main__':
    main()