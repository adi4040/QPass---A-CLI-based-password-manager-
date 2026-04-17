from pymongo import MongoClient
import argparse
from initialization import is_initialized, set_master_password
from crud_operations import add_details, get_details, delete_details, get_vault_details
from vault import create_vault, load_vault
from auth import login, logout
from session_configs import SESSION
import os 
from check_mongo import get_mongo_uri, save_mongo_uri

uri = get_mongo_uri()
if not uri: 
    print("First-time setup: MongoDB URI required..(MongoDB Atlas)")
    uri = input("Enter your MongoDB URI: ").strip()
    save_mongo_uri(uri)
    print("Mongo URI saved!\n")


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

add_uri = subparsers.add_parser("add_mongo_uri")
add_uri.add_argument("mongo_uri")

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

    elif args.command == "add_mongo_uri":
        update_mongo_uri(args.mongo_uri)

    else: 
        print("Unknown command, type \"help\" for command list")

def update_mongo_uri(new_uri): 

    global client, db
    new_uri = args.mongo_uri
    client = MongoClient(new_uri)
    db = client['Qpass']
    print("Mongo URI updated and reconnected.")


def require_login():
    if not SESSION['key']: 
        return False
    else: return True

def show_help(): 
    print("""
Commands:
        ulogin
        ulogout
        add <site> <password> (add a site)
        get <site> (details of a site) 
        delete <site> (delete a site)
        get_vault (data from vault)
        get_site <site> (details about particular site)
        create_vault (creates a vault)
        add_mongo_uri <uri> (add/update your mongodb connection uri)
        clear (clears the output)
        exit
    """)
     

def show_banner():
    from session_configs import SESSION

    status = "🔓 Logged In" if SESSION["key"] else "Not Logged In"

    print(rf"""
  ____   ____                    
 / __ \ / __ \____  ____  ____  
/ / / // /_/ / __ \/ __ \/ __ \ 
/ /_/ // ____/ /_/ / /_/ / /_/ / 
\____//_/    \____/\____/\____/  

        Q P A S S

QPass - Secure Password Manager
By Aditya Suryawanshi

Status: {status}

Type 'help' for commands | 'exit' to quit
""")

if __name__ == "__main__": 

    
    if not is_initialized(db): 
        set_master_password(db)

    print("QPass Interactive CLI (type 'exit' to quit)")

    show_banner()

    while True: 

        try: 
            command = input("qpass> ").strip()

            if not command: 
                continue
                
            if command in ["exit", "quit"]: 
                print("goodbye, buddy..")
                break

            if command == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                continue

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
        

