import socket
import threading
import logging
from utils.logger import setup_logger

logger = setup_logger('server')

class TCPServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def handle_client(self, conn, addr):
        with conn:
            logger.info(f"Connected by {addr}")
            try:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    logger.debug(f"Received: {data.decode()}")
                    conn.sendall(b"Server received your message")
            except Exception as e:
                logger.error(f"Error handling client: {e}", exc_info=True)
            finally:
                logger.info(f"Disconnected by {addr}")

    def start(self):
        self.sock.listen()
        logger.info(f'Server listening on {self.host}:{self.port}')
        while True:
            conn, addr = self.sock.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    server = TCPServer()
    server.start()