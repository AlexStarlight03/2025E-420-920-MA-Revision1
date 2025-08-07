
def export_account_postings(data, account_name, filename):
    file = open(filename, 'w', encoding='utf-8')
    file.write("No txn,Date,Compte,Montant,Commentaire\n")
    for transaction in data:
        if transaction.compte == account_name:
            line = f"{transaction.no_txn},{transaction.date},{transaction.compte},{transaction.montant},{transaction.commentaire}\n"
            file.write(line)
    file.close()
    print(f"Écritures exportées vers {filename}")

def validate_account_name(accounts, account_name):
    for account in accounts:
        if account.lower() == account_name.lower():
            return account
    print(f"Compte '{account_name}' introuvable!")
    print("Vérifiez l'orthographe ou choisissez un compte dans la liste.") 
    return None

def handle_balance_inquiry(account):
    print("\n--- Consultation de solde ---")
    account.display_all_accounts()
    
    while True:
        account_input = input("\nEntrez le nom du compte: ").strip()
    
        if not account_input:
            print("Nom de compte invalide!")
            continue
    
        validated_account = validate_account_name(account.accounts, account_input)
    
        if not validated_account:
            continue
    
        balance = account.calculate_balance(validated_account)
        print(f"\nSolde du compte '{validated_account}': {balance:.2f}$")
        return

def handle_statistics(account):
    print("\n=== STATISTIQUES FINANCIÈRES ===")
    
    total_income = account.find_total_income()
    total_expenses = account.find_total_expenses()
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
    
    largest_expense = account.find_largest_expense()
    if largest_expense:
        print(f"\nPlus grosse dépense: {largest_expense.montant:.2f}$ ({largest_expense.compte})")
        if largest_expense.commentaire:
            print(f"Commentaire: {largest_expense.commentaire}")
    
    current_account_balance = account.calculate_balance('Compte courant')
    print(f"\nSolde du compte courant: {current_account_balance:.2f}$")

def handle_date_search(account):
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
    
    filtered_data = account.get_transactions_by_date_range(start_date, end_date)
    
    if len(filtered_data) == 0:
        print(f"Aucune transaction trouvée entre {start_date} et {end_date}")
    else:
        print(f"\n{len(filtered_data)} écritures(s) trouvée(s) entre {start_date} et {end_date}:")
        for transaction in filtered_data:
            print(f"  {transaction.date} - {transaction.compte}: {transaction.montant:.2f}$")

def handle_export(account):
    print("\n--- Exportation ---")
    account.display_all_accounts()
    
    while True:
        account_input = input("\nEntrez le nom du compte à exporter: ").strip()
    
        if not account_input:
            print("Nom de compte invalide! Essayez à nouveau.")
            continue
    
        validated_account = validate_account_name(account.accounts, account_input)
    
        if validated_account:
            filename = input("Nom du fichier de sortie (ex: export.csv): ").strip()
            if not filename:
                filename = f"export_{validated_account.replace(' ', '_').lower()}.csv"
        
            export_account_postings(account.transactions, validated_account, filename)
            break