import socket
import threading
from .logger import logger

class TCPServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.server = None
        self.lock = threading.Lock()

    def start(self):
        """Start the TCP server with multi-threading."""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            logger.info(f"Server listening on {self.host}:{self.port}")
            while True:
                client, address = self.server.accept()
                logger.info(f"Accepted connection from {address}")
                client_thread = threading.Thread(target=self.handle_client, args=(client,))
                client_thread.start()
        except Exception as e:
            logger.error(f"Server failed to start: {e}")
        finally:
            if self.server:
                self.server.close()

    def handle_client(self, client_socket):
        """Handle client connections."""
        with self.lock:  # Ensure thread-safe operations if needed
            try:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    # Process data here
                    client_socket.sendall(b"Received your message")
            except Exception as e:
                logger.error(f"Error handling client: {e}")
            finally:
                client_socket.close()

# Usage would typically be in a main or application startup script
# server = TCPServer()
# server.start()