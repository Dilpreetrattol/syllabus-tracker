#!/usr/bin/env python3
"""
List all users in the database with their details.
Usage: python scripts/list_users.py
"""

from app import create_app, db
from app.models import User
from tabulate import tabulate

def main():
    app = create_app()
    with app.app_context():
        users = User.query.all()
        
        if not users:
            print("No users found in the database.")
            return
        
        # Prepare data for table display
        headers = ["ID", "Name", "Email", "Role", "Department", "Phone", "Active", "Created"]
        rows = []
        
        for user in users:
            rows.append([
                user.id,
                user.name,
                user.email,
                user.role,
                user.department or "N/A",
                user.phone or "N/A",
                "Yes" if user.is_active else "No",
                user.created_at.strftime("%Y-%m-%d %H:%M") if user.created_at else "N/A"
            ])
        
        print(f"\nFound {len(users)} user(s):")
        print("=" * 80)
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        
        # Show role distribution
        role_counts = {}
        for user in users:
            role_counts[user.role] = role_counts.get(user.role, 0) + 1
        
        print("\nRole Distribution:")
        print("-" * 20)
        for role, count in role_counts.items():
            print(f"{role.capitalize()}: {count}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the database is created and accessible.")