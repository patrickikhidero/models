import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('banking_system.db', check_same_thread=False)
        self.create_users_table()

    def create_users_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    account_number TEXT UNIQUE NOT NULL,
                    balance REAL NOT NULL
                )
            ''')

    def add_user(self, username, account_number, balance):
        with self.connection:
            self.connection.execute('INSERT INTO users (username, account_number, balance) VALUES (?, ?, ?)', 
                                    (username, account_number, balance))

    def update_balance(self, username, amount):
        with self.connection:
            self.connection.execute('UPDATE users SET balance = balance + ? WHERE username = ?', (amount, username))

    def get_balance(self, username):
        cursor = self.connection.cursor()
        cursor.execute('SELECT balance FROM users WHERE username = ?', (username,))
        return cursor.fetchone()

    def get_user_account(self, username):
        cursor = self.connection.cursor()
        cursor.execute('SELECT account_number, balance FROM users WHERE username = ?', (username,))
        return cursor.fetchone()
