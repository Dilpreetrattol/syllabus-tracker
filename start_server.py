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
    
    # Build the correct gunicorn command
    cmd = [
        'gunicorn',
        'app:app',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '1',
        '--timeout', '120',
        '--keepalive', '2',
        '--max-requests', '1000',
        '--preload'
    ]
    
    print(f"Starting server on port {port}")
    print(f"Command: {' '.join(cmd)}")
    
    # Execute gunicorn
    os.execvp('gunicorn', cmd)

if __name__ == '__main__':
    main()