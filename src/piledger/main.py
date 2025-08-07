import os
import csv
from piledger.transaction import Transaction
from piledger.account import Account
from piledger.handling import handle_balance_inquiry, validate_account_name, handle_statistics, handle_export, handle_date_search

def read_data_file():
    data : list[Transaction] = []
    with open('data.csv', 'r', newline='', encoding='utf-8') as file:
        transactions = csv.DictReader(file)
        for line in transactions:
            trans_toadd = Transaction(int(line['No txn']), line['Date'], line['Compte'], float(line['Montant']), line['Commentaire'])
            data.append(trans_toadd)
    return data

def get_all_accounts(data):
    accounts = []
    for transaction in data:
        account_type = transaction.compte
        if account_type not in accounts:
            accounts.append(account_type)
    return accounts

def display_menu():
    print("\n" + "="*50)
    print("SYSTÈME DE GESTION COMPTABLE PERSONNEL")
    print("="*50)
    print("1. Afficher le solde d'un compte")
    print("2. Afficher toutes les transactions")
    print("3. Afficher les transactions d'un compte")
    print("4. Afficher le résumé de tous les comptes")
    print("5. Afficher les statistiques")
    print("6. Exporter les écritures d'un compte")
    print("7. Rechercher par période")
    print("0. Quitter")
    print("="*50)

def main():
    print("Chargement des données...")
    
    if not os.path.exists('data.csv'):
        print("ERREUR: Le fichier data.csv est introuvable!")
        print("Assurez-vous que le fichier se trouve à la racine du répertoire.")
        return
    
    data = read_data_file()
    
    if len(data) == 0:
        print("ERREUR: Aucune donnée n'a pu être chargée!")
        return
    
    print(f"✅ {len(data)} transactions chargées avec succès!")
    
    account = Account(data, get_all_accounts(data))

    while True:
        display_menu()
        
        try:
            choice = input("\nVotre choix: ").strip()
        except:
            print("\nAu revoir!")
            break
        # TODO PERFECT MOMENT TO ADD A SWITCH CASE
        if choice == "1":
            handle_balance_inquiry(account)
        elif choice == "2":
            account.display_all_transactions()
        elif choice == "3":
            print("\n--- Transactions par compte ---")
            account.display_all_accounts()
            
            while True:
                account_input = input("\nEntrez le nom du compte: ").strip()
                
                if account_input:
                    validated_account = validate_account_name(account.accounts, account_input)
                    if validated_account:
                        account.display_transactions_by_account(validated_account)
                        break
                else:
                    print("Nom de compte invalide!")
        elif choice == "4":
            account.display_summary()
        elif choice == "5":
            handle_statistics(account)
        elif choice == "6":
            handle_export(account)
        elif choice == "7":
            handle_date_search(account)
        elif choice == "0":
            print("\nMerci d'avoir utilisé le système de gestion comptable!")
            print("Au revoir!")
            break
        else:
            print("❌ Choix invalide! Veuillez sélectionner une option valide.")
            continue
        
        input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()