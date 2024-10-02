# app/models.py
import sqlite3


def create_tables():
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        balance REAL DEFAULT 0
    )
    """)
    
    conn.commit()
    conn.close()

create_tables()
