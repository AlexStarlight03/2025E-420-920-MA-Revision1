
from piledger.transaction import Transaction
class Account():
    # Initialization
    def __init__(self, transactions : list, accounts : list):
        self.transactions = transactions
        self.accounts = accounts

        self._acc_balances = {}
        self._stats = None

    # Display methods
    def display_all_transactions(self):
        print("\n=== TOUTES LES TRANSACTIONS ===")
        if not self.transactions:
            print("Aucune transaction trouvée.")
            return
        for transaction in self.transactions:
            transaction.afficher()
    
    def display_all_accounts(self):
        print("Comptes disponibles:")
        if not self.transactions:
            print("Aucun compte trouvé.")
            return
        for acc in self.accounts:
            print(f"  - {acc}")

    def display_transactions_by_account(self, account_name):
        print(f"\n=== TRANSACTIONS POUR LE COMPTE '{account_name}' ===")
        transactions = self.get_transactions_by_account(account_name)
        if not transactions:
            print(f"Aucune transaction trouvée pour le compte '{account_name}'")
            return
        for transacc in transactions:
                transacc.afficher_sanscompte()

    def display_summary(self):
        print("\n=== RÉSUMÉ DES COMPTES ===")
        for acc in self.accounts:
            balance = self.calculate_balance(acc)
            print(f"{acc}: {balance:.2f}$")

    # Data retrieval methods
    def get_transactions_by_date_range(self, start_date, end_date):
        return [fil_t for fil_t in self.transactions if start_date <= fil_t.date <= end_date]
    
    def get_transactions_by_account(self, account_name):
        return [t for t in self.transactions if t.compte == account_name]
    
    # Calculation methods
    def calculate_balance(self, account_name):
        if account_name in self._acc_balances:
            return self._acc_balances[account_name]
        balance = sum(t.montant for t in self.transactions if t.compte == account_name)
        self._acc_balances[account_name] = balance
        return balance

    def _find_largest_expense(self):
        largest_expense = None
        expenses = [t for t in self.transactions if t.montant > 0 and t.compte not in ['Compte courant', 'Revenu']]
        return max(expenses, key=lambda t: t.montant, default=None) #TODO understand this

    def _find_total_income(self):
        return sum(abs(t.montant) for t in self.transactions if t.compte == "Revenu")

    def _find_total_expenses(self):
        return sum(t.montant for t in self.transactions if t.compte not in ['Compte courant', 'Revenu'])
    
    # Getter for stats
    def get_stats(self):
        if self._stats is not None:
            return self._cached_stats
            
        income = self._find_total_income()
        expenses = self._find_total_expenses()
        largest_expense = self._find_largest_expense()
        
        self._stats = {
            'total_income': income,
            'total_expenses': expenses,
            'largest_expense': largest_expense,
            'current_account_balance': self.calculate_balance('Compte courant'),
            'net_worth': income - expenses,
        }
        return self._stats
    
    def __str__(self) -> str:
        return f"Account Manager: {len(self.accounts)} accounts, {len(self.transactions)} transactions"

