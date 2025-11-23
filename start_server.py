#!/usr/bin/env python3
"""
Production startup script for Render deployment
"""
import os
import sys
import subprocess
import traceback

def main():
    """Start the application with proper gunicorn configuration"""
    try:
        print("🚀 Starting Render deployment...")
        print(f"🐍 Python version: {sys.version}")
        print(f"📂 Current working directory: {os.getcwd()}")
        print(f"📁 Files in directory: {os.listdir('.')}")
        
        port = os.environ.get('PORT', '10000')
        print(f"🌐 Port: {port}")
        
        # Check if app.py exists
        if not os.path.exists('app.py'):
            print("❌ app.py file not found!")
            sys.exit(1)
        else:
            print("✅ app.py found")
        
        # Debug: Check if app.py can be imported
        try:
            print("🔍 Testing app import...")
            import app
            print(f"✅ Successfully imported app module")
            print(f"✅ App instance found: {hasattr(app, 'app')}")
            if hasattr(app, 'app'):
                print(f"✅ App type: {type(app.app)}")
            else:
                print("❌ No 'app' attribute in app module")
                print(f"Available attributes: {[attr for attr in dir(app) if not attr.startswith('_')]}")
        except Exception as e:
            print(f"❌ Failed to import app: {e}")
            print(f"Error traceback: {traceback.format_exc()}")
            sys.exit(1)
        
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
        
        print(f"🚀 Starting server on port {port}")
        print(f"📝 Command: {' '.join(cmd)}")
        
        # Execute gunicorn
        os.execvp('gunicorn', cmd)
        
    except Exception as e:
        print(f"💥 Fatal error in start_server.py: {e}")
        print(f"📋 Full traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == '__main__':
    main()