import socket
import json

def display_dashboard(username):
    while True:
        print("\n--- Dashboard ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Transfer")
        print("4. Get Balance")
        print("5. Exit")
        option = input("Choose an option: ")

        if option == "1":
            amount = float(input("Enter amount to deposit: "))
            request = {"action": "deposit", "username": username, "amount": amount}
        elif option == "2":
            amount = float(input("Enter amount to withdraw: "))
            request = {"action": "withdraw", "username": username, "amount": amount}
        elif option == "3":
            transfer_to = input("Enter username to transfer to: ")
            amount = float(input("Enter amount to transfer: "))
            request = {"action": "transfer", "from_user": username, "to_user": transfer_to, "amount": amount}
        elif option == "4":
            request = {"action": "get_balance", "username": username}
        elif option == "5":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")
            continue

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 5000))  # Connect to the server
            s.sendall(json.dumps(request).encode())
            response = s.recv(1024).decode()
            print("Response from server:", response)

if __name__ == "__main__":
    username = input("Enter your username to log in: ")
    display_dashboard(username)
