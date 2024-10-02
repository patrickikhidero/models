import socket

def client(action, account_id, amount, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', server_port))
        message = f"{action},{amount},{account_id}"
        s.sendall(message.encode())
        response = s.recv(1024).decode()
        print(response)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: python client.py <action> <account_id> <amount> <server_port>")
        sys.exit(1)
    action, account_id, amount, server_port = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
    client(action, account_id, amount, server_port)
