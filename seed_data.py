"""
seed_data.py — Mock Data Seeder for Expense Tracker
-----------------------------------------------------
Run this script ONCE to populate the database with realistic demo data.
Usage:
    python seed_data.py

Creates:
    - 2 demo user accounts
    - 60+ realistic expense entries spread across the last 3 months
"""

from datetime import date, timedelta
import random
from app import create_app, db
from app.models.user import User
from app.models.expense import Expense

# ── Demo User Accounts ─────────────────────────────────────────────────────────
DEMO_USERS = [
    {"username": "demo_user",  "email": "demo@example.com",  "password": "Demo@1234"},
    {"username": "john_doe",   "email": "john@example.com",  "password": "John@1234"},
]

# ── Realistic Expense Data per Category ────────────────────────────────────────
EXPENSE_TEMPLATES = [
    # (category, description, min_amount, max_amount)
    ("Food & Dining",     "Lunch at restaurant",         8.0,   35.0),
    ("Food & Dining",     "Grocery shopping",           30.0,  120.0),
    ("Food & Dining",     "Coffee & snacks",             3.0,   15.0),
    ("Food & Dining",     "Dinner with friends",        20.0,   80.0),
    ("Food & Dining",     "Food delivery order",        15.0,   45.0),

    ("Transportation",    "Uber / Cab ride",             8.0,   30.0),
    ("Transportation",    "Monthly bus pass",           40.0,   60.0),
    ("Transportation",    "Petrol / Fuel refill",       25.0,   70.0),
    ("Transportation",    "Parking fee",                 3.0,   15.0),

    ("Housing & Rent",    "Monthly rent payment",      600.0, 1200.0),
    ("Housing & Rent",    "Home maintenance",           50.0,  200.0),
    ("Housing & Rent",    "Cleaning supplies",          10.0,   40.0),

    ("Utilities",         "Electricity bill",           40.0,   90.0),
    ("Utilities",         "Internet bill",              30.0,   60.0),
    ("Utilities",         "Water & sewage bill",        15.0,   35.0),
    ("Utilities",         "Mobile phone bill",          20.0,   50.0),

    ("Entertainment",     "Movie tickets",              12.0,   30.0),
    ("Entertainment",     "Concert / Event tickets",   30.0,  120.0),
    ("Entertainment",     "Video game purchase",        20.0,   70.0),
    ("Entertainment",     "Board game / hobby",        15.0,   50.0),

    ("Shopping",          "Clothing purchase",          25.0,  150.0),
    ("Shopping",          "Electronics accessory",      15.0,  200.0),
    ("Shopping",          "Online shopping order",      20.0,  100.0),
    ("Shopping",          "Home decor item",            20.0,   80.0),

    ("Healthcare",        "Doctor visit / consultation",30.0,  120.0),
    ("Healthcare",        "Pharmacy / medicines",       10.0,   60.0),
    ("Healthcare",        "Gym membership",             25.0,   80.0),
    ("Healthcare",        "Health supplement",          15.0,   50.0),

    ("Education",         "Online course subscription", 15.0,   50.0),
    ("Education",         "Books / study materials",    10.0,   60.0),
    ("Education",         "Tuition / coaching fee",    100.0,  300.0),

    ("Travel",            "Flight ticket",             120.0,  500.0),
    ("Travel",            "Hotel accommodation",        60.0,  200.0),
    ("Travel",            "Travel insurance",           15.0,   50.0),
    ("Travel",            "Tourist activity / tour",    20.0,  100.0),

    ("Personal Care",     "Haircut / salon visit",      15.0,   60.0),
    ("Personal Care",     "Skincare products",          10.0,   50.0),
    ("Personal Care",     "Personal hygiene items",      5.0,   25.0),

    ("Subscriptions",     "Netflix subscription",       10.0,   18.0),
    ("Subscriptions",     "Spotify Premium",             8.0,   12.0),
    ("Subscriptions",     "Cloud storage plan",          2.0,   10.0),
    ("Subscriptions",     "Software / SaaS tool",       10.0,   50.0),

    ("Other",             "Charity donation",           10.0,   50.0),
    ("Other",             "Gift for someone",           15.0,  100.0),
    ("Other",             "Miscellaneous expense",       5.0,   40.0),
]


def random_date_in_last_n_months(n_months: int = 3) -> date:
    """Return a random date within the last n months."""
    today = date.today()
    start = today - timedelta(days=n_months * 30)
    delta = (today - start).days
    return start + timedelta(days=random.randint(0, delta))


def seed():
    app = create_app()
    with app.app_context():
        print("🌱 Starting database seeding...\n")

        # ── Create Users ───────────────────────────────────────────────────────
        created_users = []
        for u_data in DEMO_USERS:
            existing = User.query.filter_by(email=u_data["email"]).first()
            if existing:
                print(f"   ⚠️  User '{u_data['username']}' already exists — skipping.")
                created_users.append(existing)
            else:
                user = User(username=u_data["username"], email=u_data["email"])
                user.set_password(u_data["password"])
                db.session.add(user)
                db.session.flush()  # get the ID before commit
                created_users.append(user)
                print(f"   ✅ Created user: {u_data['username']} ({u_data['email']})")

        db.session.commit()

        # ── Create Expenses ────────────────────────────────────────────────────
        total_added = 0
        for user in created_users:
            # Pick 30 random expense templates for each user
            chosen = random.choices(EXPENSE_TEMPLATES, k=30)
            for (category, description, min_amt, max_amt) in chosen:
                expense = Expense(
                    user_id=user.id,
                    amount=round(random.uniform(min_amt, max_amt), 2),
                    category=category,
                    description=description,
                    date=random_date_in_last_n_months(3),
                )
                db.session.add(expense)
                total_added += 1

        db.session.commit()
        print(f"\n   💰 Added {total_added} expense records across {len(created_users)} users.")

        # ── Summary ────────────────────────────────────────────────────────────
        print("\n" + "─" * 50)
        print("✅ Seeding complete! You can now log in with:")
        for u in DEMO_USERS:
            print(f"   📧 Email: {u['email']}  |  🔑 Password: {u['password']}")
        print("─" * 50)
        print("🌐 Open: http://127.0.0.1:5000\n")


if __name__ == "__main__":
    seed()
