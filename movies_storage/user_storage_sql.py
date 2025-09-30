"""
User storage module using SQLAlchemy.
Handles creating, listing, and selecting users.
"""

from sqlalchemy import create_engine, text
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "movies.db")
DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URL, echo=False)

with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """))
    connection.commit()


def list_users():
    """Return all users as (id, name)."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, name FROM users"))
        return result.fetchall()


def add_user(name):
    """Add a new user to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("INSERT INTO users (name) VALUES (:name)"),
                {"name": name}
            )
            connection.commit()
            print(f"User '{name}' created successfully.")
        except Exception as e:
            print(f"⚠️ Error creating user: {e}")


def get_user(user_id):
    """Fetch a single user by ID."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT id, name FROM users WHERE id = :id"),
            {"id": user_id}
        ).fetchone()
        return result


def select_user():
    """
    Ask the user to select an existing profile or create a new one.
    Returns (user_id, username).
    """
    while True:
        users = list_users()

        print("\nWelcome to the Movie App! 🎬")
        print("Select a user:")
        for idx, (uid, name) in enumerate(users, start=1):
            print(f"{idx}. {name}")
        print(f"{len(users) + 1}. Create new user")

        choice = input("Enter choice: ").strip()

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(users):
                user_id, username = users[choice - 1]
                print(f"\nWelcome back, {username}! 🎬")
                return user_id, username
            elif choice == len(users) + 1:
                new_name = input("Enter new username: ").strip()
                if not new_name:
                    print("Username cannot be empty.")
                    continue
                add_user(new_name)
                with engine.connect() as connection:
                    result = connection.execute(
                        text("SELECT id FROM users WHERE name = :name"),
                        {"name": new_name}
                    ).fetchone()
                    return result[0], new_name

        print("Invalid choice, please try again.")