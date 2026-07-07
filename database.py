import sqlite3


def get_connection():
    conn = sqlite3.connect("portfolio.db")

    # Dictionary ki tarah data return karega
    conn.row_factory = sqlite3.Row

    return conn
import os

def get_connection():
    db_path = os.path.abspath("portfolio.db")
    print("Using database:", db_path)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn