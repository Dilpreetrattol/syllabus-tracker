import argparse
import sys

from app import create_app, db
from app.models import User


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Add a test/user account to the database")
    parser.add_argument("--name", required=False, default="Test User", help="Full name")
    parser.add_argument("--email", required=False, default="test.user@example.com", help="Email address (unique)")
    parser.add_argument("--password", required=False, default="Test123!", help="Password")
    parser.add_argument(
        "--role",
        required=False,
        default="student",
        choices=["student", "teacher", "hod", "coordinator"],
        help="User role",
    )
    parser.add_argument("--department", required=False, default="CSE", help="Department code/name")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    app = create_app()
    with app.app_context():
        existing = User.query.filter_by(email=args.email).first()
        if existing:
            print(f"User already exists: {existing.email} (id={existing.id}, role={existing.role})")
            return 0

        user = User(
            name=args.name,
            email=args.email,
            role=args.role,
            department=args.department,
            user_metadata={"seeded": True},
        )
        user.set_password(args.password)

        db.session.add(user)
        db.session.commit()

        print("User created successfully:")
        print(f"  id        : {user.id}")
        print(f"  name      : {user.name}")
        print(f"  email     : {user.email}")
        print(f"  role      : {user.role}")
        print(f"  department: {user.department}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
