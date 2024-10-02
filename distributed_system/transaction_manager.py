class TransactionManager:
    def __init__(self, db):
        self.db = db

    def deposit(self, username, amount):
        self.db.update_balance(username, amount)
        return {"status": "success", "message": f"Deposited {amount} to {username}'s account."}

    def withdraw(self, username, amount):
        balance = self.db.get_balance(username)
        if balance and balance[0] >= amount:
            self.db.update_balance(username, -amount)
            return {"status": "success", "message": f"Withdrew {amount} from {username}'s account."}
        return {"status": "error", "message": "Insufficient funds."}

    def transfer(self, from_user, to_user, amount):
        from_balance = self.db.get_balance(from_user)
        if from_balance and from_balance[0] >= amount:
            self.db.update_balance(from_user, -amount)
            self.db.update_balance(to_user, amount)
            return {"status": "success", "message": f"Transferred {amount} from {from_user} to {to_user}."}
        return {"status": "error", "message": "Insufficient funds."}
