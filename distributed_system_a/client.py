import socket
import json

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_transaction(self, account_id, amount):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            transaction = {
                "type": "transaction",
                "data": {"account_id": account_id, "amount": amount}
            }
            s.sendall(json.dumps(transaction).encode('utf-8'))
            data = s.recv(1024)
        return json.loads(data.decode('utf-8'))

if __name__ == "__main__":
    client = Client('localhost', 9999)
    response = client.send_transaction(1, -50)  # Example: withdraw 50 from account 1
    print(response)