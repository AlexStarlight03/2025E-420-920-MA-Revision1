

class Transaction():
    def __init__(self, notxn : int, date : str, compte : str, montant : float, commentaire : str):
        self.no_txn = notxn
        self.date = date
        self.compte = compte
        self.montant = montant
        if commentaire.strip() is not None: 
            self.commentaire = commentaire
    
    def afficher(self):
        print(f"Transaction {self.no_txn} - {self.date}")
        print(f"  Compte: {self.compte}")
        print(f"  Montant: {self.montant}$")
        if self.commentaire:
            print(f"  Commentaire: {self.commentaire}")
        print()
    
    def afficher_sanscompte(self):
        print(f"Transaction {self.no_txn} - {self.date}")
        print(f"  Montant: {self.montant:.2f}$")
        if self.commentaire:
            print(f"  Commentaire: {self.commentaire}")
        print()

    def __str__(self):
        return self.afficher()
