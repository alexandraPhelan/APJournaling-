
import os
import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "apjournaling.db"


def init_db():
    # In secure version we recreate the DB with hashed passwords
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # SECURE: password column stores HASH, not plaintext
    cur.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )

    hashed_pw = generate_password_hash("password123")
    cur.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        ("testuser", "test@example.com", hashed_pw),
    )

    conn.commit()
    conn.close()
    print("Secure database initialised:", DB_PATH)


if __name__ == "__main__":
    init_db()
