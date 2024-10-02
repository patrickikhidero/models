from database_manager import DatabaseManager

class TransactionCoordinator:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.transaction_id = 0

    def initiate_transaction(self, transaction_data):
        self.transaction_id += 1
        if self._prepare_phase(transaction_data):
            print(True)
            if self._commit_phase():
                return {"status": "success", "message": "Transaction committed"}
        self._rollback_phase()
        return {"status": "error", "message": "Transaction failed"}

    def _prepare_phase(self, transaction_data):
        # Here you would lock resources or prepare transaction
        # For simplicity, we're just checking if the transaction is valid
        if self._is_valid_transaction(transaction_data):
            return True
        return False

    def _commit_phase(self):
        # Actually commit the transaction in all databases
        return self.db_manager.execute("UPDATE accounts SET balance = ? WHERE id = ?", 
                                       (transaction_data['amount'], transaction_data['account_id']))

    def _rollback_phase(self):
        # Rollback changes if any were made
        self.db_manager.conn.rollback()

    def _is_valid_transaction(self, data):
        # Basic validation
        current_balance = self.db_manager.fetchone("SELECT balance FROM accounts WHERE id = ?", (data['account_id'],))
        if current_balance and current_balance[0] + data['amount'] >= 0:
            return True
        return False