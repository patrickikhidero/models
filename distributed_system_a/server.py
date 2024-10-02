import socket
from threading import Thread
import json
from transaction_coordinator import TransactionCoordinator
from database_manager import DatabaseManager

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.db_manager = DatabaseManager('bank.db')
        self.coordinator = TransactionCoordinator(self.db_manager)

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client, address = self.sock.accept()
            client_handler = Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    def handle_client(self, client_socket):
        with client_socket:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                return
            request = json.loads(data)
            response = self.process_request(request)
            client_socket.send(json.dumps(response).encode('utf-8'))

    def process_request(self, request):
        if request['type'] == 'transaction':
            return self.coordinator.initiate_transaction(request['data'])
        return {"status": "error", "message": "Unknown request type"}

if __name__ == "__main__":
    server = Server('localhost', 9999)
    server.start()