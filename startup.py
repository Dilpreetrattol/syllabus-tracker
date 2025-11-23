#!/usr/bin/env python3
"""
Startup script for production deployment
Provides better error handling and debugging
"""
import sys
import os

def main():
    try:
        print("🚀 Starting Syllabus Tracker application...")
        
        # Check critical environment variables
        secret_key = os.environ.get('SECRET_KEY')
        database_url = os.environ.get('DATABASE_URL')
        
        print(f"✅ SECRET_KEY: {'Set' if secret_key else 'Missing'}")
        print(f"✅ DATABASE_URL: {'Set' if database_url else 'Missing'}")
        
        if not secret_key:
            print("❌ ERROR: SECRET_KEY environment variable is required")
            sys.exit(1)
            
        # Import and create the app
        from app import create_app
        app = create_app()
        
        print("✅ Flask app created successfully")
        print(f"📊 Database URI: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
        
        # Test database connection
        with app.app_context():
            from app import db
            try:
                # Try to connect to database
                db.engine.execute("SELECT 1")
                print("✅ Database connection successful")
            except Exception as e:
                print(f"❌ Database connection failed: {e}")
                # Continue anyway, might work with auto-creation
        
        return app
        
    except Exception as e:
        print(f"❌ Application startup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    app = main()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))