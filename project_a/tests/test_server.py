# Example in test_server.py
def test_server_start():
    server = TCPServer('localhost', 9999)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    # Here you would typically connect to the server to ensure it's running
    server_thread.join(timeout=1)
    assert not server_thread.is_alive(), "Server did not start correctly"