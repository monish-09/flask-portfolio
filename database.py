import sqlite3


def get_connection():
    conn = sqlite3.connect("portfolio.db")

    # Dictionary ki tarah data return karega
    conn.row_factory = sqlite3.Row

    return conn