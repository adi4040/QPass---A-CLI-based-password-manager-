import argparse
import os
import sys
import time
import threading
from pathlib import Path
from pymongo import MongoClient

from .initialization import is_initialized, set_master_password
from .crud_operations import add_details, get_details, delete_details, get_vault_details
from .vault import create_vault, load_vault
from .auth import login, logout
from .session_configs import SESSION
from .check_mongo import get_mongo_uri, save_mongo_uri


def spinner_running(flag):
    symbols = ['|', '/', '-', '\\']
    i = 0
    while flag["running"]:
        sys.stdout.write(f"\r... {symbols[i % len(symbols)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1



def setup_mongo():
    uri = get_mongo_uri()

    if not uri:
        url = "https://www.mongodb.com/cloud/atlas/register"
        link_text = "Click here"
        formatted_link = f"\033]8;;{url}\033\\{link_text}\033]8;;\033\\"

        print(f"First-time setup: {formatted_link} to set up MongoDB Atlas")

        while True:
            uri = input("Enter your MongoDB URI: ").strip()

            print("Verifying your URI...")

            flag = {"running": True}
            t = threading.Thread(target=spinner_running, args=(flag,))
            t.start()

            try:
                client = MongoClient(uri)
                client.admin.command('ping')
                client.close()

                flag["running"] = False
                t.join()

                print("\rVerified successfully.          ")
                save_mongo_uri(uri)
                break

            except Exception:
                flag["running"] = False
                t.join()
                print("\rInvalid Mongo URI. Try again.   ")

    # final connection
    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        print("Connected to MongoDB")
        return client
    except Exception:
        print("Stored Mongo URI is invalid. Resetting...")
        config_path = Path.home() / ".qpass_config.json"
        if config_path.exists():
            config_path.unlink()
        print("Restart QPass and enter a valid URI.")
        sys.exit()



def require_login():
    return bool(SESSION.get("key"))


def show_help():
    print("""
Commands:
    ulogin
    ulogout
    add <site> <password>
    delete <site>
    get_vault
    get_site <site>
    create_vault
    load_vault
    add_mongo_uri <uri>
    clear
    exit
""")


def show_banner():
    status = "Logged In" if SESSION.get("key") else "Not Logged In"
    print(rf"""
  ____   ____                    
 / __ \ / __ \____  ____  ____  
/ / / // /_/ / __ \/ __ \/ __ \ 
/ /_/ // ____/ /_/ / /_/ / /_/ / 
\____//_/    \____/\____/\____/  

        Q P A S S

QPass - Secure Password Manager

Status: {status}

Type 'help' for commands | 'exit' to quit
""")



def update_mongo_uri(new_uri):
    print("Verifying your URI...")

    flag = {"running": True}
    t = threading.Thread(target=spinner_running, args=(flag,))
    t.start()

    try:
        client = MongoClient(new_uri)
        client.admin.command('ping')

        flag["running"] = False
        t.join()

        save_mongo_uri(new_uri)
        print("Mongo URI updated successfully.")
        return client

    except Exception:
        flag["running"] = False
        t.join()
        print("Invalid Mongo URI. Keeping previous connection.")
        return None



def handle_commands(args, db, client):
    if args.command == "add":
        add_details(args, db)

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
        show_banner()

    elif args.command == "ulogout":
        logout()
        show_banner()

    elif args.command == "help":
        show_help()

    elif args.command == "add_mongo_uri":
        new_client = update_mongo_uri(args.mongo_uri)
        if new_client:
            return new_client, new_client['Qpass']

    else:
        print("Unknown command. Type 'help'.")

    return client, db



def build_parser():
    parser = argparse.ArgumentParser(prog="qpass", add_help=False)
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("site")
    add_parser.add_argument("password")

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("site")

    subparsers.add_parser("create_vault")
    subparsers.add_parser("load_vault")
    subparsers.add_parser("get_vault")

    get_site = subparsers.add_parser("get_site")
    get_site.add_argument("site")

    subparsers.add_parser("ulogin")
    subparsers.add_parser("ulogout")

    add_uri = subparsers.add_parser("add_mongo_uri")
    add_uri.add_argument("mongo_uri")

    subparsers.add_parser("help")

    return parser



def main():
    client = setup_mongo()
    db = client["Qpass"]

    if not is_initialized(db):
        set_master_password(db)

    parser = build_parser()

    print("QPass Interactive CLI")
    show_banner()

    while True:
        try:
            command = input("qpass> ").strip()

            if not command:
                continue

            if command in ["exit", "quit"]:
                print("Goodbye.")
                break

            if command == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                show_banner()
                continue

            args = parser.parse_args(command.split())

            if args.command in ["add", "delete", "get_vault", "get_site"]:
                if not require_login():
                    print("Please login first.")
                    continue

            client, db = handle_commands(args, db, client)

        except SystemExit:
            print("Invalid input")

        except Exception as e:
            print(f"Error: {e}")