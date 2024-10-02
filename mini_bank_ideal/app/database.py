# app/database.py
import sqlite3
from contextlib import closing

DATABASE_URL = "sqlite:///./bank.db"

def get_db():
    conn = sqlite3.connect("bank.db")
    with closing(conn):
        yield conn


