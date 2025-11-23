from app import create_app

app = create_app()

# Auto-create database tables on startup (for Railway deployment)
def init_db():
    try:
        from app import db
        with app.app_context():
            db.create_all()
            print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️  Database initialization error: {e}")

# Initialize database on import
with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=False)