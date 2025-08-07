import csv
from datetime import datetime

def check_exit(command):
    """Check if user entered an exit command"""
    if command in ['exit', 'quit', 'no', 'bye']:
        print("\nMerci d'avoir utilisé le système de gestion comptable!")
        print("Au revoir!")
        return True
    return False

def validate_account_name(accounts, account_name):
    """Validate if account exists"""
    for account in accounts:
        if account.lower() == account_name.lower():
            return account
    print(f"❌ Compte '{account_name}' introuvable!")
    print("Vérifiez l'orthographe ou choisissez un compte dans la liste.") 
    return None

def handle_balance_inquiry(account):
    """Check balance of a specific account"""
    print("\n--- Consultation de solde ---")
    account.display_all_accounts()
    while True:
        account_input = input("\nEntrez le nom du compte: ").strip()
        if check_exit(account_input):
            return "0"
        if not account_input:
            print("❌ Nom de compte invalide!")
            continue
        validated_account = validate_account_name(account.accounts, account_input)
        if not validated_account:
            continue
        balance = account.calculate_balance(validated_account)
        print(f"\nSolde du compte '{validated_account}': {balance:.2f}$")
        return

def handle_statistics(account):
    """Display all financial statistics"""
    print("\n=== STATISTIQUES FINANCIÈRES ===")
    stats = account.get_stats()
    total_income = stats['total_income']
    total_expenses = stats['total_expenses']
    net_worth = stats['net_worth']
    largest_expense = stats['largest_expense']
    current_account_balance = stats['current_account_balance']
    print(f"Revenus totaux: {total_income:.2f}$")
    print(f"Dépenses totales: {total_expenses:.2f}$")
    print(f"Situation nette: {net_worth:.2f}$")
    if net_worth > 0:
        print("📈 Situation financière positive")
    elif net_worth < 0:
        print("📉 Situation financière négative")
    else:
        print("⚖️  Situation financière équilibrée")
    if largest_expense:
        print(f"\nPlus grosse dépense: {largest_expense.montant:.2f}$ ({largest_expense.compte})")
        if largest_expense.commentaire:
            print(f"Commentaire: {largest_expense.commentaire}")
    print(f"\nSolde du compte courant: {current_account_balance:.2f}$")


def valid_date(input):
    """Check if date is in the right format and if it's valid."""
    try:
        datetime.strptime(input, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def input_date(type):
    """Asks user to input date. Checks validity and exit command."""
    while True:
        date = input(f"Date de {type} (YYYY-MM-DD): ").strip()
        if check_exit(date):
            return
        if valid_date(date):
            return date
        print("❌ Date invalide! Essayez à nouveau.")

def handle_date_search(account):
    """Search all transaction made from specific dates"""
    print("\n--- Recherche par période ---")
    start_date = input_date("début")
    if not start_date:
        return "0"
    end_date = input_date("fin")
    if not end_date:
        return "0"
    if start_date > end_date:
        print("⚠️  La date de fin est antérieure à la date de début. Échange automatique.")
        start_date, end_date = end_date, start_date
    filtered_data = account.get_transactions_by_date_range(start_date, end_date)
    if not filtered_data:
        print(f"Aucune transaction trouvée entre {start_date} et {end_date}")
    else:
        print(f"\n{len(filtered_data)} écritures(s) trouvée(s) entre {start_date} et {end_date}:")
        for transaction in filtered_data:
            print(f"  {transaction.date} - {transaction.compte}: {transaction.montant:.2f}$")

def export_account_postings(data, filename):
    """Exports to a csv file all transaction from a specific account."""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["No txn", "Date", "Compte", "Montant", "Commentaire"])
            for transaction in data:
                writer.writerow([transaction.no_txn, transaction.date, transaction.compte, transaction.montant, transaction.commentaire])
        print(f"Écritures exportées vers {filename}")
    except IOError as e:
        print(f"❌ Erreur lors de l'exportation: {e}")

def handle_export(account):
    """Choose a valid account to export it's data."""
    print("\n--- Exportation ---")
    account.display_all_accounts()
    while True:
        account_input = input("\nEntrez le nom du compte à exporter: ").strip()
        if check_exit(account_input):
            return "0"
        if not account_input:
            print("Nom de compte invalide! Essayez à nouveau.")
            continue
        validated_account = validate_account_name(account.accounts, account_input)
        if validated_account:
            filename = input("Nom du fichier de sortie (ex: export.csv): ").strip()
            if not filename:
                filename = f"export_{validated_account.replace(' ', '_').lower()}.csv"
            filename += "."
            export_account_postings(account.get_transactions_by_account(validated_account), filename)
            break