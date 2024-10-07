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