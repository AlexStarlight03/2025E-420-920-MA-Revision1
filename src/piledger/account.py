

class Account():
    def __init__(self, transactions : list, accounts : list):
        self.transactions = transactions
        self.accounts = accounts
   
    # def afficher(self):
    #     print(f"Transaction {self.no_txn} - {self.date}")
    #     print(f"  Compte: {self.compte}")
    #     print(f"  Montant: {self.montant}$")
    #     if self.commentaire:
    #         print(f"  Commentaire: {self.commentaire}")
    #     print()
    
    # def afficher_sanscompte(self):
    #     print(f"Transaction {self.no_txn} - {self.date}")
    #     print(f"  Montant: {self.montant:.2f}$")
    #     if self.commentaire:
    #         print(f"  Commentaire: {self.commentaire}")
    #     print()

    # def __str__(self):
    #     return self.afficher()