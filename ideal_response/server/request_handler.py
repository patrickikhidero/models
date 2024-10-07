import socket
from utils.logger import Logger
from utils.security import SecurityManager

class RequestHandler:
    def __init__(self, client_socket, client_address, security_manager):
        self.client_socket = client_socket
        self.client_address = client_address
        self.security_manager = security_manager
        self.logger = Logger(__name__)

    def handle(self):
        try:
            data = self.client_socket.recv(1024).decode('utf-8')
            if not data:
                return

            sanitized_data = self.security_manager.sanitize_input(data)
            self.logger.info(f"Received data from {self.client_address}: {sanitized_data}")

            # Process the request (example)
            response = self.process_request(sanitized_data)

            encrypted_response = self.security_manager.encrypt_data(response)
            self.client_socket.sendall(encrypted_response)
            self.logger.info(f"Sent response to {self.client_address}")

        except socket.error as e:
            self.logger.error(f"Socket error: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error handling request: {str(e)}")

    def process_request(self, data):
        # This is a placeholder for request processing logic
        # Implement your specific request handling here
        return f"Processed: {data}"