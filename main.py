from pymongo import MongoClient
import argparse
from initialization import is_initialized, set_master_password
from crud_operations import add_details, get_details, delete_details, get_vault_details
from vault import create_vault, load_vault
from auth import login, logout
from session_configs import SESSION

uri = "mongodb+srv://adityasuryawanshi4040_db_user:Iamadam4040@pythonpract.hncczo8.mongodb.net/?appName=PythonPract"

client = MongoClient(uri)
db = client['Qpass']


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")


add_parser = subparsers.add_parser("add")
add_parser.add_argument("site")
add_parser.add_argument("password")

get_parser = subparsers.add_parser("get")
get_parser.add_argument("gmail")

delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("site")

create_v = subparsers.add_parser("create_vault") 
# create_vault.add_argument("create_vault")
load_v = subparsers.add_parser("load_vault")

get_v = subparsers.add_parser("get_vault")


get_site = subparsers.add_parser("get_site")
get_site.add_argument("site")

ulogin = subparsers.add_parser("ulogin")
ulogout = subparsers.add_parser("ulogout")

help = subparsers.add_parser("help")


def handle_commands(args, db): 


    if args.command == "add": 
        add_details(args, db)

    elif args.command == "get": 
        get_details(db)

    elif args.command == "delete": 
        delete_details(args, db)

    elif args.command == "create_vault": 
        create_vault(db)

    elif args.command == "load_vault": 
        load_vault(db)


    elif args.command == "get_vault": 
        get_details(db)

    elif args.command == "get_site": 
        get_vault_details(args, db)


    elif args.command == "ulogin": 
        login(db)

    elif args.command == "ulogout": 
        logout()

    elif args.command == "help":
        show_help()

    else: 
        print("Unknown command, type \"help\" for command list")



def require_login():
    if not SESSION['key']: 
        return False
    else: return True

def show_help(): 
    print("""
Commands:
        ulogin
        ulogout
        add <gmail> <password>
        get <gmail>
        delete <site>
        get_vault
        get_site <site>
        create_vault
        exit
    """)
     

if __name__ == "__main__": 
    
    
    if not is_initialized(db): 
        set_master_password(db)

    

    print("QPass Interactive CLI (type 'exit' to quit)")

    while True: 

        try: 
            command = input("qpass> ").strip()

            if not command: 
                continue
                
            if command in ["exit", "quit"]: 
                print("goodbye, buddy..")
                break

            args = parser.parse_args(command.split())
            if args.command in ["add", "get", "delete", "get_vault", "get_site"]:
                if not require_login(): 
                    print("Please login first..")
                    continue 

            handle_commands(args, db)

        except SystemExit: 
            print("Invalid input")
        
        except Exception as e: 
            print(f"Error: {e}")
        

