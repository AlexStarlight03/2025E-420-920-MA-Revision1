import os
import csv
from collections import defaultdict
from piledger.transaction import Transaction
from piledger.account import Account

def read_data_file():
    data : list[Transaction] = []
    with open('data.csv', 'r', newline='', encoding='utf-8') as file:
        transactions = csv.DictReader(file)
        for line in transactions:
            trans_toadd = Transaction(int(line['No txn']), line['Date'], line['Compte'], float(line['Montant']), line['Commentaire'])
            data.append(trans_toadd)
    return data

def calculate_balance(data, account_name):
    balance : float = 0
    for transaction in data:
        if transaction.compte == account_name:
            balance += transaction.montant
    return balance

def get_all_accounts(data):
    accounts = []
    for transaction in data:
        account_type = transaction.compte
        if account_type not in accounts:
            accounts.append(account_type)
    return accounts

def display_all_transactions(data):
    print("\n=== TOUTES LES TRANSACTIONS ===")
    for transaction in data:
        transaction.afficher()

def display_transactions_by_account(data, account_name): #TODO combine with a function that takes modular nb of parameters!
    print(f"\n=== TRANSACTIONS POUR LE COMPTE '{account_name}' ===")
    found_any = False 
    for transaction in data:
        if transaction.compte == account_name:
            found_any = True
            transaction.afficher_sanscompte()
    if not found_any:
        print(f"Aucune transaction trouvée pour le compte '{account_name}'")

def display_summary(data):
    print("\n=== RÉSUMÉ DES COMPTES ===")
    accounts = get_all_accounts(data)
    for account in accounts:
        balance = calculate_balance(data, account)
        print(f"{account}: {balance:.2f}$")


def get_transactions_by_date_range(data, start_date, end_date):
    filtered_transactions = []
    for transaction in data:
        if start_date <= transaction.date <= end_date:
            filtered_transactions.append(transaction)
    return filtered_transactions

def find_largest_expense(data):
    largest_expense = None
    max_amount = 0
    for transaction in data: # TODO: surely can find a easier way, automatic find ??
        if transaction.montant > max_amount and transaction.compte != 'Compte courant' and transaction.compte != 'Revenu':
            max_amount = transaction.montant
            largest_expense = transaction
    return largest_expense

def find_total_income(data):
    total = 0
    for transaction in data:
        if transaction.compte == 'Revenu':
            total += abs(transaction.montant)
    return total

def find_total_expenses(data):
    total = 0
    for transaction in data: # TODO: add something for courant and revenu to find easier
        if transaction.compte != 'Compte courant' and transaction.compte != 'Revenu' and transaction.montant > 0:
            total += transaction.montant
    return total

def export_account_postings(data, account_name, filename): #TODO: Find how create csv file better than this
    file = open(filename, 'w', encoding='utf-8')
    file.write("No txn,Date,Compte,Montant,Commentaire\n")
    for transaction in data:
        if transaction.compte == account_name:
            line = f"{transaction.no_txn},{transaction.date},{transaction.compte},{transaction.montant},{transaction.commentaire}\n"
            file.write(line)
    file.close()
    print(f"Écritures exportées vers {filename}")

def validate_account_name(accounts, account_name): #TODO check how simplify
    for account in accounts:
        if account.lower() == account_name.lower():
            return account
    print(f"Compte '{account_name}' introuvable!")
    print("Vérifiez l'orthographe ou choisissez un compte dans la liste.") 
    return None

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

def handle_balance_inquiry(data, accounts):
    print("\n--- Consultation de solde ---")
    print("Comptes disponibles:")
    for account in accounts:
        print(f"  - {account}")
    
    while True:
        account_input = input("\nEntrez le nom du compte: ").strip()
    
        if not account_input: #TODO : add better check and not a return but add a loop!!!
            print("Nom de compte invalide!")
            continue
    
        validated_account = validate_account_name(accounts, account_input)
    
        if not validated_account:
            # break loop and return to entering account name
            continue
    
        balance = calculate_balance(data, validated_account)
        print(f"\nSolde du compte '{validated_account}': {balance:.2f}$")
        return # or break ?? TODO


def handle_statistics(data):
    print("\n=== STATISTIQUES FINANCIÈRES ===")
    
    total_income = find_total_income(data)
    total_expenses = find_total_expenses(data)
    net_worth = total_income - total_expenses
    
    print(f"Revenus totaux: {total_income:.2f}$")
    print(f"Dépenses totales: {total_expenses:.2f}$")
    print(f"Situation nette: {net_worth:.2f}$")
    
    if net_worth > 0: # TODO Would a switch case be better ?
        print("📈 Situation financière positive")
    elif net_worth < 0:
        print("📉 Situation financière négative")
    else:
        print("⚖️  Situation financière équilibrée")
    
    largest_expense = find_largest_expense(data)
    if largest_expense:
        print(f"\nPlus grosse dépense: {largest_expense.montant:.2f}$ ({largest_expense.compte})")
        if largest_expense.commentaire:
            print(f"Commentaire: {largest_expense.commentaire}")
    
    current_account_balance = calculate_balance(data, 'Compte courant')
    print(f"\nSolde du compte courant: {current_account_balance:.2f}$")

def handle_date_search(data): #TODO: CHECK IF DATES ARE ACTUAL DATES......
    print("\n--- Recherche par période ---")
    while True:
        start_date = input("Date de début (YYYY-MM-DD): ").strip()
        if start_date:
            break
        print("Date invalide! Essayez à nouveau.")
    while True:
        end_date = input("Date de fin (YYYY-MM-DD): ").strip()
        if end_date:
            break
        print("Date invalide! Essayez à nouveau.")
    
    filtered_data = get_transactions_by_date_range(data, start_date, end_date)
    
    if len(filtered_data) == 0: # TODO: or if not filtered_data ??
        print(f"Aucune transaction trouvée entre {start_date} et {end_date}")
    else:
        print(f"\n{len(filtered_data)} écritures(s) trouvée(s) entre {start_date} et {end_date}:")
        for transaction in filtered_data:
            print(f"  {transaction.date} - {transaction.compte}: {transaction.montant:.2f}$")

def handle_export(data, accounts):
    print("\n--- Exportation ---")
    print("Comptes disponibles:")
    for account in accounts:
        print(f"  - {account}")
    
    while True:
        account_input = input("\nEntrez le nom du compte à exporter: ").strip()
    
        if not account_input:
            print("Nom de compte invalide! Essayez à nouveau.")
            continue
    
        validated_account = validate_account_name(accounts, account_input)
    
        if validated_account:
            filename = input("Nom du fichier de sortie (ex: export.csv): ").strip()
            if not filename:
                filename = f"export_{validated_account.replace(' ', '_').lower()}.csv"
        
            export_account_postings(data, validated_account, filename)
            break


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
        # TODO PERFECT MOMENT TO ADD A SWITCH CASE HEREEEEE
        if choice == "1":
            handle_balance_inquiry(account.transactions, account.accounts)
        elif choice == "2":
            display_all_transactions(account.transactions)
        elif choice == "3":
            print("\n--- Transactions par compte ---")
            print("Comptes disponibles:")
            for account in account.accounts: #instead print list account.accounts
                print(f"  - {account}")
            
            while True:
                account_input = input("\nEntrez le nom du compte: ").strip()
                
                if account_input:
                    validated_account = validate_account_name(account.accounts, account_input)
                    if validated_account:
                        display_transactions_by_account(account.transactions, validated_account)
                        break
                else:
                    print("Nom de compte invalide!")
        elif choice == "4":
            display_summary(account.transactions)
        elif choice == "5":
            handle_statistics(account.transactions)
        elif choice == "6":
            handle_export(account.transactions, account.accounts)
        elif choice == "7":
            handle_date_search(account.transactions)
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