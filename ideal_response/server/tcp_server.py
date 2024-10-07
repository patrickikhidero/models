import socket
import threading
import ssl
from concurrent.futures import ThreadPoolExecutor
from .request_handler import RequestHandler
from utils.logger import Logger
from utils.security import SecurityManager

class TCPServer:
    def __init__(self, host, port, max_connections=10, use_ssl=False):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.use_ssl = use_ssl
        self.logger = Logger(__name__)
        self.security_manager = SecurityManager()
        self.socket = None
        self.thread_pool = ThreadPoolExecutor(max_workers=max_connections)

    def start(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.max_connections)

            if self.use_ssl:
                self.socket = self._wrap_socket_ssl(self.socket)

            self.logger.info(f"Server started on {self.host}:{self.port}")

            while True:
                client_socket, address = self.socket.accept()
                self.logger.info(f"New connection from {address}")
                self.thread_pool.submit(self._handle_client, client_socket, address)

        except Exception as e:
            self.logger.error(f"Server error: {str(e)}")
        finally:
            self.stop()

    def stop(self):
        if self.socket:
            self.socket.close()
        self.thread_pool.shutdown(wait=True)
        self.logger.info("Server stopped")

    def _handle_client(self, client_socket, address):
        try:
            handler = RequestHandler(client_socket, address, self.security_manager)
            handler.handle()
        except Exception as e:
            self.logger.error(f"Error handling client {address}: {str(e)}")
        finally:
            client_socket.close()

    def _wrap_socket_ssl(self, sock):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="path/to/cert.pem", keyfile="path/to/key.pem")
        return context.wrap_socket(sock, server_side=True)