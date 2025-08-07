
class Account():
    def __init__(self, transactions : list, accounts : list):
        self.transactions = transactions
        self.accounts = accounts


    def display_all_transactions(self):
        print("\n=== TOUTES LES TRANSACTIONS ===")
        for transaction in self.transactions:
            transaction.afficher()
    
    def display_all_accounts(self):
        print("Comptes disponibles:")
        for acc in self.accounts:
            print(f"  - {acc}")

    def display_transactions_by_account(self, account_name):
        print(f"\n=== TRANSACTIONS POUR LE COMPTE '{account_name}' ===")
        found_any = False 
        for transaction in self.transactions:
            if transaction.compte == account_name:
                found_any = True
                transaction.afficher_sanscompte()
        if not found_any:
            print(f"Aucune transaction trouvée pour le compte '{account_name}'")

    def calculate_balance(self, account_name):
        balance : float = 0
        for transaction in self.transactions:
            if transaction.compte == account_name:
                balance += transaction.montant
        return balance
    
    def display_summary(self):
        print("\n=== RÉSUMÉ DES COMPTES ===")
        for acc in self.accounts:
            balance = self.calculate_balance(acc)
            print(f"{acc}: {balance:.2f}$")
    
    def find_largest_expense(self):
        largest_expense = None
        max_amount = 0
        for transaction in self.transactions:
            if transaction.montant > max_amount and transaction.compte != 'Compte courant' and transaction.compte != 'Revenu':
                max_amount = transaction.montant
                largest_expense = transaction
        return largest_expense

    def find_total_income(self):
        total = 0
        for transaction in self.transactions:
            if transaction.compte == 'Revenu':
                total += abs(transaction.montant)
        return total

    def find_total_expenses(self):
        total = 0
        for transaction in self.transactions:
            if transaction.compte != 'Compte courant' and transaction.compte != 'Revenu' and transaction.montant > 0:
                total += transaction.montant
        return total
    
    def get_transactions_by_date_range(self, start_date, end_date):
        filtered_transactions = []
        for transaction in self.transactions:
            if start_date <= transaction.date <= end_date:
                filtered_transactions.append(transaction)
        return filtered_transactions