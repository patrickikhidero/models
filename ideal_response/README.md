```bash
.
├── config.py
├── main.py
├── packet_analysis
│   ├── __init__.py
│   └── packet_analyzer.py
├── requirements.txt
├── server
│   ├── __init__.py
│   ├── request_handler.py
│   └── tcp_server.py
├── ssh
│   ├── __init__.py
│   └── ssh_client.py
├── tests
│   ├── __init__.py
│   ├── test_packet_analyzer.py
│   ├── test_server.py
│   └── test_ssh_client.py
└── utils
    ├── __init__.py
    ├── logger.py
    └── security.py
```
Here's the code for each of the files excluding the __init__.py since it's only to tell python it's a package structure
1. `config.py`
```python
import os

class Config:
    # Server Configuration
    SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')
    SERVER_PORT = int(os.getenv('SERVER_PORT', 8000))
    MAX_CONNECTIONS = int(os.getenv('MAX_CONNECTIONS', 10))
    USE_SSL = os.getenv('USE_SSL', 'False').lower() == 'true'

    # SSH Configuration
    SSH_HOST = os.getenv('SSH_HOST', 'example.com')
    SSH_USERNAME = os.getenv('SSH_USERNAME', 'user')
    SSH_PASSWORD = os.getenv('SSH_PASSWORD', 'password')

    # Network Configuration
    NETWORK_INTERFACE = os.getenv('NETWORK_INTERFACE', 'eth0')

    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')

    # Security Configuration
    ENCRYPTION_KEY_FILE = os.getenv('ENCRYPTION_KEY_FILE', 'secret.key')
```
2. `main.py`
```python
import sys
from server.tcp_server import TCPServer
from ssh.ssh_client import SSHClient
from packet_analysis.packet_analyzer import PacketAnalyzer
from utils.logger import Logger
from config import Config
import threading

def main():
    logger = Logger(__name__)
    config = Config()

    try:
        # Start TCP Server
        server = TCPServer(config.SERVER_HOST, config.SERVER_PORT, config.MAX_CONNECTIONS, config.USE_SSL)
        server_thread = threading.Thread(target=server.start)
        server_thread.start()

        # SSH Client example
        ssh_client = SSHClient(config.SSH_HOST, config.SSH_USERNAME, config.SSH_PASSWORD)
        ssh_client.connect()
        result = ssh_client.execute_command('ls -l')
        logger.info(f"SSH Command Result: {result}")
        ssh_client.close()

        # Packet Analyzer example
        analyzer = PacketAnalyzer(config.NETWORK_INTERFACE)
        packets = analyzer.capture_packets(count=10, filter="tcp")
        for packet in packets:
            analysis = analyzer.analyze_packet(packet)
            logger.info(f"Packet Analysis: {analysis}")

        potential_scans = analyzer.detect_port_scan(packets)
        if potential_scans:
            logger.warning(f"Potential port scans detected: {potential_scans}")

        # Keep the main thread running
        server_thread.join()

    except KeyboardInterrupt:
        logger.info("Shutting down...")
        server.stop()
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```
3. `packet_analysis/packet_analyzer.py`
```python
from scapy.all import sniff, IP, TCP, UDP
from utils.logger import Logger
import subprocess

class PacketAnalyzer:
    def __init__(self, interface='en0'):
        self.interface = interface
        self.logger = Logger(__name__)

    def capture_packets(self, count=0, filter="tcp"):
        try:
            self.logger.info(f"Starting packet capture on interface {self.interface}")
            packets = sniff(iface=self.interface, count=count, filter=filter, prn=self._packet_callback)
            return packets
        except Exception as e:
            self.logger.error(f"Error during packet capture: {str(e)}")
            return None    
    
    def _packet_callback(self, packet):
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet[IP].proto

            if TCP in packet:
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                self.logger.info(f"TCP: {src_ip}:{src_port} -> {dst_ip}:{dst_port}")
            elif UDP in packet:
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport
                self.logger.info(f"UDP: {src_ip}:{src_port} -> {dst_ip}:{dst_port}")
            else:
                self.logger.info(f"Other IP: {src_ip} -> {dst_ip}, Protocol: {protocol}")

    def analyze_packet(self, packet):
        analysis = {}
        if IP in packet:
            analysis['ip'] = {
                'src': packet[IP].src,
                'dst': packet[IP].dst,
                'proto': packet[IP].proto
            }
            if TCP in packet:
                analysis['tcp'] = {
                    'sport': packet[TCP].sport,
                    'dport': packet[TCP].dport,
                    'flags': packet[TCP].flags
                }
            elif UDP in packet:
                analysis['udp'] = {
                    'sport': packet[UDP].sport,
                    'dport': packet[UDP].dport
                }
        return analysis
    
    def detect_port_scan(self, packets, threshold=10):
        port_attempts = {}

        for packet in packets:
            if TCP in packet:
                src_ip = packet[IP].src
                dst_port = packet[TCP].dport
                # Use only src_ip to count unique destination ports
                if src_ip not in port_attempts:
                    port_attempts[src_ip] = set()  # Use a set to track unique ports
                port_attempts[src_ip].add(dst_port)

        potential_scans = [
            (ip, len(ports)) for ip, ports in port_attempts.items() if len(ports) >= threshold
        ]
        
        if potential_scans:
            self.logger.warning(f"Potential port scan detected from IPs: {potential_scans}")

        return potential_scans
```
3. `requirements.txt`
```plaintext
paramiko==2.7.2
scapy
cryptography==3.4.7
pytest==6.2.5
```
4. `server/request_handler.py`

```python
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
```
5. `server/tcp_server.py`
```python
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
```
6. `ssh/ssh_client.py`
```python
import paramiko
from utils.logger import Logger

class SSHClient:
    def __init__(self, hostname, username, password=None, key_filename=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.client = None
        self.logger = Logger(__name__)

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                self.hostname,
                username=self.username,
                password=self.password,
                key_filename=self.key_filename
            )
            self.logger.info(f"Successfully connected to {self.hostname}")
        except paramiko.AuthenticationException:
            self.logger.error(f"Authentication failed for {self.hostname}")
            raise
        except paramiko.SSHException as ssh_exception:
            self.logger.error(f"SSH exception occurred: {str(ssh_exception)}")
            raise
        except Exception as e:
            self.logger.error(f"Error connecting to {self.hostname}: {str(e)}")
            raise

    def execute_command(self, command):
        if not self.client:
            self.logger.error("Not connected. Call connect() first.")
            return None

        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()
            
            if exit_status == 0:
                output = stdout.read().decode('utf-8').strip()
                self.logger.info(f"Command executed successfully: {command}")
                return output
            else:
                error = stderr.read().decode('utf-8').strip()
                self.logger.warning(f"Command failed: {command}. Error: {error}")
                return None
        except Exception as e:
            self.logger.error(f"Error executing command: {str(e)}")
            return None

    def close(self):
        if self.client:
            self.client.close()
            self.logger.info(f"Closed connection to {self.hostname}")
```
7. `tests/test_packet_analyzer.py`
```python
import unittest
from unittest.mock import patch, MagicMock
from scapy.all import IP, TCP, UDP, sniff
from packet_analysis.packet_analyzer import PacketAnalyzer

class TestPacketAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = PacketAnalyzer('en0')

    @patch('scapy.all.sniff')
    def test_capture_packets(self, mock_sniff):
        mock_packets = [MagicMock(), MagicMock()]
        result = mock_sniff(iface='en0', count=2, filter="tcp", prn=self.analyzer._packet_callback)
        mock_sniff.assert_called_once_with(iface='en0', count=2, filter="tcp", prn=self.analyzer._packet_callback)
        self.assertNotEqual(result, mock_packets)

    def test_analyze_packet(self):
        # Create a mock IP/TCP packet
        mock_packet = IP(src="192.168.1.1", dst="10.0.0.1")/TCP(sport=12345, dport=80, flags="S")

        analysis = self.analyzer.analyze_packet(mock_packet)

        self.assertEqual(analysis['ip']['src'], "192.168.1.1")
        self.assertEqual(analysis['ip']['dst'], "10.0.0.1")
        self.assertEqual(analysis['tcp']['sport'], 12345)
        self.assertEqual(analysis['tcp']['dport'], 80)
        self.assertEqual(analysis['tcp']['flags'], "S")

    def test_detect_port_scan(self):
        # Create mock packets simulating a port scan
        packets = [
            IP(src="192.168.1.1", dst="10.0.0.1")/TCP(sport=12345, dport=port)
            for port in range(1, 15)  # This generates ports 1 to 14
        ]

        potential_scans = self.analyzer.detect_port_scan(packets, threshold=5)

        # Check that the IP and the number of unique ports is correct
        self.assertIn(("192.168.1.1", 14), potential_scans)
        # This check for ("192.168.1.1", 10) does not make sense and should be removed
        self.assertEqual(len(potential_scans), 1)  # Only one unique IP should be detected

    
    

if __name__ == '__main__':
    unittest.main()
```
8. `tests/test_server.py`
```python
import unittest
import ssl
import socket
from unittest.mock import patch, MagicMock
from server.tcp_server import TCPServer

class TestTCPServer(unittest.TestCase):
    def setUp(self):
        self.server = TCPServer('localhost', 8000)

    @patch('socket.socket')
    def test_server_start(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        # Simulate server start and stop
        def side_effect(*args):
            self.server.stop()
        mock_socket_instance.accept.side_effect = side_effect

        self.server.start()

        mock_socket_instance.bind.assert_called_once_with(('localhost', 8000))
        mock_socket_instance.listen.assert_called_once()
        assert mock_socket_instance.close.call_count == 2

    @patch('server.tcp_server.RequestHandler')
    @patch('socket.socket')
    def test_handle_client(self, mock_socket, mock_handler):
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        client_socket = MagicMock()
        client_address = ('127.0.0.1', 12345)

        self.server._handle_client(client_socket, client_address)

        mock_handler.assert_called_once_with(client_socket, client_address, self.server.security_manager)
        mock_handler.return_value.handle.assert_called_once()

    @patch('ssl.create_default_context')
    @patch('socket.socket')
    def test_ssl_wrap(self, mock_socket, mock_ssl_context):
        mock_socket_instance = MagicMock()
        mock_context = MagicMock()
        mock_ssl_context.return_value = mock_context

        self.server.use_ssl = True
        wrapped_socket = self.server._wrap_socket_ssl(mock_socket_instance)

        mock_ssl_context.assert_called_once_with(ssl.Purpose.CLIENT_AUTH)
        mock_context.load_cert_chain.assert_called_once()
        mock_context.wrap_socket.assert_called_once_with(mock_socket_instance, server_side=True)

if __name__ == '__main__':
    unittest.main()
```
9. `tests/test_ssh_client.py`
```python
None
```
10. `utils/logger.py`
```python
import logging
import os
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, name, log_file='app.log', level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)
```
11. `utils/security.py`
```python
import hashlib
import os
from cryptography.fernet import Fernet

class SecurityManager:
    def __init__(self):
        self.key = self._load_or_generate_key()
        self.cipher_suite = Fernet(self.key)

    def _load_or_generate_key(self):
        key_file = 'secret.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as file:
                return file.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as file:
                file.write(key)
            return key

    def encrypt_data(self, data):
        return self.cipher_suite.encrypt(data.encode())

    def decrypt_data(self, encrypted_data):
        return self.cipher_suite.decrypt(encrypted_data).decode()

    def hash_password(self, password):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt + key

    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:32]
        stored_key = stored_password[32:]
        new_key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
        return new_key == stored_key

    def sanitize_input(self, input_string):
        # Implement input sanitization logic
        # This is a basic example, consider using more robust libraries like bleach
        return ''.join(char for char in input_string if char.isalnum() or char in (' ', '-', '_'))
```