"""Dangerous: Drop and recreate all tables (development only).

Usage (PowerShell):
  $env:PYTHONPATH = 'D:\syllabus-tracker-fresh'
  python .\scripts\reset_db.py --yes

Optional reseed afterwards:
  $env:SEED = '1'
  python .\scripts\create_db.py

Notes:
- This uses SQLAlchemy's metadata (drop_all/create_all). Ensure models are importable.
- Only run in development; this will delete ALL data.
"""

import argparse
from app import create_app, db


def parse_args():
    p = argparse.ArgumentParser(description="Drop and recreate all tables (DEV ONLY)")
    p.add_argument("--yes", action="store_true", help="Skip interactive confirmation")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    app = create_app()
    with app.app_context():
        uri = app.config.get("SQLALCHEMY_DATABASE_URI")
        print(f"[info] Target DB URI: {uri}")

        if not args.yes:
            print("[abort] This will DELETE ALL DATA. Re-run with --yes to confirm.")
            return 1

        # Ensure all models are loaded so metadata knows all tables
        import app.models  # noqa: F401

        print("[step] Dropping all tables...")
        db.drop_all()
        print("[ok] All tables dropped.")

        print("[step] Creating all tables...")
        db.create_all()
        print("[ok] All tables created.")

        return 0


if __name__ == "__main__":
    raise SystemExit(main())
