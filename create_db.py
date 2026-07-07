import sqlite3
from werkzeug.security import generate_password_hash

def create_database():
    conn = sqlite3.connect("portfolio.db")
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

    # Create default admin only if table is empty
    cursor.execute("SELECT COUNT(*) FROM admin")
    count = cursor.fetchone()[0]

    if count == 0:
        username = "admin"
        email = "monishkhan.projects@gmail.com"   # <-- apna email yahan likho
        password = generate_password_hash("Monish954876")

        cursor.execute("""
            INSERT INTO admin (username, email, password)
            VALUES (?, ?, ?)
        """, (username, email, password))

        print("✅ Default admin created.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("✅ Database initialized successfully.")