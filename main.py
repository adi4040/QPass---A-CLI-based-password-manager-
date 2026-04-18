from pymongo import MongoClient
import argparse
from initialization import is_initialized, set_master_password
from crud_operations import add_details, get_details, delete_details, get_vault_details
from vault import create_vault, load_vault
from auth import login, logout
from session_configs import SESSION
import os
import json
from check_mongo import get_mongo_uri, save_mongo_uri
import sys
import time
import threading


def spinner_running(flag):
    symbols = ['|', '/', '-', '\\']
    i = 0
    while flag["running"]:
        sys.stdout.write(f"\r... {symbols[i % len(symbols)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1


uri = get_mongo_uri()

if not uri:
    print("First-time setup: MongoDB URI required..(MongoDB Atlas)")

    while True:
        uri = input("Enter your MongoDB URI: ").strip()

        print("Verifying your URI... If it takes longer, the URI may be incorrect.")

        flag = {"running": True}
        t = threading.Thread(target=spinner_running, args=(flag,))
        t.start()

        try:
            test_client = MongoClient(uri)
            test_client.admin.command('ping')
            test_client.close()

            flag["running"] = False
            t.join()

            print("\rVerified successfully.            ")

            save_mongo_uri(uri)
            break

        except Exception:
            flag["running"] = False
            t.join()

            print("\rInvalid Mongo URI. Try again.     ")


try:
    client = MongoClient(uri)
    client.admin.command('ping')
    print("Connected to MongoDB")
except Exception:
    print("Stored Mongo URI is invalid.")
    if os.path.exists("config.json"):
        os.remove("config.json")
    print("Please restart and enter a valid URI.")
    exit()

db = client['Qpass']

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

add_parser = subparsers.add_parser("add")
add_parser.add_argument("site")
add_parser.add_argument("password")

delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("site")

create_v = subparsers.add_parser("create_vault")
load_v = subparsers.add_parser("load_vault")

get_v = subparsers.add_parser("get_vault")

get_site = subparsers.add_parser("get_site")
get_site.add_argument("site")

ulogin = subparsers.add_parser("ulogin")
ulogout = subparsers.add_parser("ulogout")

add_uri = subparsers.add_parser("add_mongo_uri")
add_uri.add_argument("mongo_uri")

help_cmd = subparsers.add_parser("help")


def handle_commands(args, db):
    
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
        update_mongo_uri(args.mongo_uri)
    else:
        print("Unknown command, type \"help\" for command list")


def update_mongo_uri(new_uri):
    global client, db

    print("Verifying your URI... If it takes longer, the URI may be incorrect.")

    flag = {"running": True}
    t = threading.Thread(target=spinner_running, args=(flag,))
    t.start()

    try:
        new_client = MongoClient(new_uri)
        new_client.admin.command('ping')
        flag['running'] = False
        t.join()
        save_mongo_uri(new_uri)
        client = new_client
        db = client['Qpass']
        print("Mongo URI updated and saved.")

    except Exception:
        flag["running"] = False
        t.join()
        print("Invalid Mongo URI. Keeping previous connection.")


def require_login():
    return bool(SESSION['key'])


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
        add_mongo_uri <uri>
        clear
        exit
    """)


def show_banner():
    status = "Logged In" if SESSION["key"] else "Not Logged In"
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
                show_banner()
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
            print(f"Error a: {e}")