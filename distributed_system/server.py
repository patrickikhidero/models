import socket
import threading
import json
import sqlite3
from database import Database
from transaction_manager import TransactionManager

def handle_client(connection, transaction_manager):
    with connection:
        request_data = connection.recv(1024).decode()
        request = json.loads(request_data)

        if request['action'] == 'deposit':
            response = transaction_manager.deposit(request['username'], request['amount'])
        elif request['action'] == 'withdraw':
            response = transaction_manager.withdraw(request['username'], request['amount'])
        elif request['action'] == 'transfer':
            response = transaction_manager.transfer(request['from_user'], request['to_user'], request['amount'])
        elif request['action'] == 'get_balance':
            balance_info = transaction_manager.db.get_user_account(request['username'])
            if balance_info:
                response = {
                    "status": "success",
                    "account_number": balance_info[0],
                    "balance": balance_info[1]
                }
            else:
                response = {"status": "error", "message": "User not found."}
        else:
            response = {"status": "error", "message": "Invalid action."}

        connection.sendall(json.dumps(response).encode())

def start_server(port):
    db = Database()
    transaction_manager = TransactionManager(db)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen()
    print(f"Server running on port {port}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, transaction_manager))
        thread.start()

def create_initial_users(db):
    try:
        db.add_user("user1", "ACCT001", 1000.0)
        db.add_user("user2", "ACCT002", 2000.0)
        print("Initial users created successfully.")
    except sqlite3.IntegrityError as e:
        print(f"User creation error: {str(e)}")

if __name__ == "__main__":
    db = Database()  # Create an instance of the database
    create_initial_users(db)  # Create initial users
    start_server(5000)  # Start the server
