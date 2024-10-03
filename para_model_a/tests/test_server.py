# tests/test_server.py
import unittest
from core.server import TCPServer

class TestTCPServer(unittest.TestCase):
    def test_server_creation(self):
        server = TCPServer('localhost', 9999)
        self.assertIsNotNone(server)

    def test_server_start(self):
        # Mock socket behavior for testing
        with unittest.mock.patch('socket.socket'):
            server = TCPServer('localhost', 9999)
            # Here you would typically start the server in a thread to test if it runs
            # This requires careful setup to avoid actual network operations in tests.

if __name__ == '__main__':
    unittest.main()