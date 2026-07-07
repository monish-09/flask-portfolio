import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "portfolio.db")


def create_database():
    print("🚀 create_database() called")
    print("DB Path:", DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Admin Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Contact Messages Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        subject TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM admin")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("""
        INSERT INTO admin (username,email,password)
        VALUES (?,?,?)
        """, (
            "admin",
            "monishkhan.projects@gmail.com",
            generate_password_hash("Monish954876")
        ))

    print("✅ Database initialized successfully")
    conn.commit()
    conn.close()