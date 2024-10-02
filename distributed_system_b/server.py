import socket
from threading import Thread
from transaction_manager import TransactionManager, TransactionState
from config import SERVER_PORTS

def handle_client(conn, tm):
    with conn:
        data = conn.recv(1024).decode()
        if data:
            action, *transaction_data = data.split(',')
            tm.start_transaction()
            conn, cursor = tm.prepare_transaction(transaction_data)
            if all(reply == "OK" for reply in [conn.recv(1024).decode() for _ in SERVER_PORTS if _ != tm.server_id]):
                tm.commit()
                conn.sendall(b"Transaction Committed")
            else:
                tm.rollback()
                conn.sendall(b"Transaction Aborted")

def server(server_id):
    tm = TransactionManager(server_id, SERVER_PORTS)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', SERVER_PORTS[server_id]))
        s.listen()
        while True:
            conn, addr = s.accept()
            Thread(target=handle_client, args=(conn, tm)).start()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python server.py <server_id>")
        sys.exit(1)
    server_id = int(sys.argv[1])
    server(server_id)