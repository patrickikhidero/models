import sqlite3
import os
from config import DB_PATH

class Database:
    def __init__(self, server_id):
        self.path = DB_PATH.format(server_id)
        if not os.path.exists(self.path):
            self._create_db()

    def _create_db(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                balance REAL NOT NULL
            )
            ''')

    def execute(self, query, params=()):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid if "INSERT" in query else cursor.fetchall()

    def prepare(self, query, params=()):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        return conn, cursor

    def commit(self, conn):
        conn.commit()

    def rollback(self, conn):
        conn.rollback()