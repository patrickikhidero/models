from enum import Enum
import socket
from database import Database

class TransactionState(Enum):
    INIT = 1
    PREPARED = 2
    COMMITTED = 3
    ABORTED = 4

class TransactionManager:
    def __init__(self, server_id, ports):
        self.server_id = server_id
        self.db = Database(server_id)
        self.ports = ports
        self.state = TransactionState.INIT

    def start_transaction(self):
        self.state = TransactionState.INIT

    def prepare_transaction(self, transaction_data):
        conn, cursor = self.db.prepare("UPDATE accounts SET balance = balance + ? WHERE id = ?", transaction_data)
        self.state = TransactionState.PREPARED
        return conn, cursor

    def broadcast(self, message, exclude_self=True):
        for port in self.ports:
            if exclude_self and port == self.ports[self.server_id]:
                continue
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', port))
                s.sendall(message.encode())

    def commit(self):
        if self.state == TransactionState.PREPARED:
            self.db.commit(self.conn)
            self.state = TransactionState.COMMITTED
            self.broadcast("COMMIT")
        else:
            raise Exception("Not in prepared state")

    def rollback(self):
        if self.state == TransactionState.PREPARED:
            self.db.rollback(self.conn)
            self.state = TransactionState.ABORTED
            self.broadcast("ABORT")

    def receive_message(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', self.ports[self.server_id]))
            s.listen()
            conn, addr = s.accept()
            with conn:
                message = conn.recv(1024).decode()
                if message == "COMMIT":
                    self.db.commit(self.conn)
                elif message == "ABORT":
                    self.db.rollback(self.conn)