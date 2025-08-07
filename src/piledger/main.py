import os
from piledger.transaction import Transaction
from piledger.account import Account
from piledger.handling import handle_balance_inquiry, validate_account_name, handle_statistics, handle_export, handle_date_search, check_exit, csv


def display_menu():
    """Printing the option menu."""
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

def programloop(account):
    """Main program loop for the 7 options of the menu and exit checks."""
    while True:
        display_menu()
        try:
            choice = input("\nVotre choix: ").strip()
        except:
            print("\nAu revoir!")
            break
        match choice:
            case "1":
                choice = handle_balance_inquiry(account)
            case "2":
                account.display_all_transactions()
            case "3":
                print("\n--- Transactions par compte ---")
                account.display_all_accounts()
                while True:
                    account_input = input("\nEntrez le nom du compte: ").strip()
                    
                    if account_input:
                        if check_exit(account_input):
                            choice = "0"
                            break
                        validated_account = validate_account_name(account.accounts, account_input)
                        if validated_account:
                            account.display_transactions_by_account(validated_account)
                            break
                    else:
                        print("❌ Nom de compte invalide!")
            case "4":
                account.display_summary()
            case "5":
                handle_statistics(account)
            case "6":
                choice = handle_export(account)
            case "7":
                choice = handle_date_search(account)
            case "0":
                print("\nMerci d'avoir utilisé le système de gestion comptable!")
                print("Au revoir!")
                break
            case _:
                if check_exit(choice):
                    break
                print("❌ Choix invalide! Veuillez sélectionner une option valide.")
        if choice == "0":
            break
        input("\nAppuyez sur Entrée pour continuer...")

def read_data_file():
    """Read the csv file provided and extracting the data."""
    data : list[Transaction] = []
    try:
        with open('data.csv', 'r', newline='', encoding='utf-8') as file:
            transactions = csv.DictReader(file)
            for line in transactions:
                try:
                    trans_toadd = Transaction(int(line['No txn']), line['Date'], line['Compte'], float(line['Montant']), line['Commentaire'])
                    data.append(trans_toadd)
                except (ValueError, KeyError) as e:
                    print(f"⚠️  Erreur dans la lecture des lignes du fichier csv: {e}")
                    continue
    except FileNotFoundError:
        print("❌ Erreur: Le fichier data.csv est introuvable!")
    except PermissionError:
        print("❌ Erreur: Permission de lecture refusée pour le fichier data.csv")
    except csv.Error as e:
        print(f"❌ Erreur de format CSV: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue lors de la lecture: {e}")
    return data

def get_all_accounts(data):
    """Getting all accounts name for the creation of user's account."""
    accounts = []
    for transaction in data:
        account_type = transaction.compte
        if account_type not in accounts:
            accounts.append(account_type)
    return accounts

def main():
    """
    Initializing program by reading csv file to get all accounts and transactions details.
    Creation of an Account class variable with all the data needed.
    Account used in the main program loop.
    """
    print("Chargement des données...")
    if not os.path.exists('data.csv'):
        print("❌ Erreur: Le fichier data.csv est introuvable!")
        print("Assurez-vous que le fichier se trouve à la racine du répertoire.")
        return
    data = read_data_file()
    if len(data) == 0:
        print("❌ ERREUR: Aucune donnée n'a pu être chargée!")
        return
    print(f"✅ {len(data)} transactions chargées avec succès!")
    try:
        account = Account(data, get_all_accounts(data))
        programloop(account)
    except Exception as e:
        print(f"❌ Erreur lors de l'éxécution du programme : {e}")
    return


if __name__ == "__main__":
    main()