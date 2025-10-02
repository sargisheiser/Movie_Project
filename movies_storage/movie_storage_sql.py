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
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT,
            note TEXT,
            imdb_id TEXT,
            country TEXT,
            soundtrack_url TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id),
            UNIQUE(user_id, title)
        )
    """))
    connection.commit()


def list_movies(user_id):
    """Retrieve all movies for a specific user."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, poster, note FROM movies WHERE user_id = :uid"),
            {"uid": user_id}
        )
        movies = result.fetchall()
    return {
        row[0]: {"year": row[1], "rating": row[2], "poster": row[3], "note": row[4]}
        for row in movies
    }


def add_movie(user_id, title, year, rating, poster, imdb_id, country, soundtrack_url):
    """Add a new movie for a specific user."""
    try:
        with engine.begin() as connection:
            connection.execute(
                text("""
                    INSERT INTO movies (user_id, title, year, rating, poster, imdb_id, country, soundtrack_url)
                    VALUES (:user_id, :title, :year, :rating, :poster, :imdb_id, :country, :soundtrack_url)
                """),
                {
                    "user_id": user_id,
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "poster": poster,
                    "imdb_id": imdb_id,
                    "country": country,
                    "soundtrack_url": soundtrack_url
                }
            )
        print(f"Movie '{title}' added successfully.")
    except Exception as e:
        print(f"Error adding movie: {e}")


def delete_movie(title, user_id):
    """Delete a movie for a specific user (only if exists)."""
    with engine.begin() as connection:
        exists = connection.execute(
            text("SELECT 1 FROM movies WHERE title = :title AND user_id = :user_id"),
            {"title": title, "user_id": user_id}
        ).fetchone()
        if not exists:
            print(f"Movie '{title}' not found for this user.")
            return
        result = connection.execute(
            text("DELETE FROM movies WHERE title = :title AND user_id = :user_id"),
            {"title": title, "user_id": user_id}
        )
        if result.rowcount:
            print(f"Movie '{title}' deleted successfully.")


def update_movie(title, rating, user_id):
    """Update a movie's rating for a specific user (only if exists)."""
    with engine.begin() as connection:
        exists = connection.execute(
            text("SELECT 1 FROM movies WHERE title = :title AND user_id = :user_id"),
            {"title": title, "user_id": user_id}
        ).fetchone()
        if not exists:
            print(f"Movie '{title}' not found for this user.")
            return
        connection.execute(
            text("UPDATE movies SET rating = :rating WHERE title = :title AND user_id = :user_id"),
            {"rating": rating, "title": title, "user_id": user_id}
        )
        print(f"Movie '{title}' updated successfully.")


def update_movie_note(user_id, title, note):
    with engine.connect() as connection:
        result = connection.execute(
            text("UPDATE movies SET note = :note WHERE user_id = :uid AND title = :title"),
            {"note": note, "uid": user_id, "title": title}
        )
        connection.commit()
        if result.rowcount:
            print(f"Movie '{title}' successfully updated with note.")
        else:
            print(f"Movie '{title}' not found for this user.")