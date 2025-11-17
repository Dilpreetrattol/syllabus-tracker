"""Simple MySQL connectivity and ORM sanity test.

Run this after activating your virtual environment to verify that:
1. The database server is reachable.
2. The specified database exists.
3. SQLAlchemy can create a session and perform a trivial query.

Usage (PowerShell):
  $env:PYTHONPATH = 'D:\syllabus-tracker-fresh'
  python .\scripts\test_db_connection.py

If the database does not exist you'll see an OperationalError. Create it:
  CREATE DATABASE syllabus_tracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""

from sqlalchemy import text
from app import create_app, db


def main() -> int:
    app = create_app()
    with app.app_context():
        uri = app.config.get("SQLALCHEMY_DATABASE_URI")
        print(f"[info] Using URI: {uri}")
        try:
            # Try a low-level connection ping
            raw_conn = db.engine.connect()
            raw_conn.execute(text("SELECT 1"))
            raw_conn.close()
            print("[ok] Low-level SELECT 1 succeeded.")
        except Exception as exc:
            print(f"[error] Connection test failed: {exc}")
            return 1

        # Check if at least one table exists
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        if not tables:
            print("[warn] No tables found. Run: python .\\scripts\\create_db.py (optionally with SEED=1)")
        else:
            print(f"[ok] Tables present: {', '.join(tables)}")

        # Try simple ORM query on User (may be empty)
        from app.models import User
        count = User.query.count()
        print(f"[info] User rows: {count}")
        if count == 0:
            print("[hint] Add a user with scripts/add_user.py or enable seeding.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
