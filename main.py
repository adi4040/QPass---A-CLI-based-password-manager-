from pymongo import MongoClient
import argparse
from initialization import is_initialized, set_master_password
from crud_operations import add_details, get_details, delete_details, get_vault_details
from vault import create_vault, load_vault

uri = "mongodb+srv://adityasuryawanshi4040_db_user:Iamadam4040@pythonpract.hncczo8.mongodb.net/?appName=PythonPract"

client = MongoClient(uri)
db = client['Qpass']


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")


add_parser = subparsers.add_parser("add")
add_parser.add_argument("gmail")
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

args = parser.parse_args()



if not is_initialized(db): 
    set_master_password(db)


if args.command == "add": 
    add_details(args, db)

if args.command == "get": 
    get_details(args, db)

if args.command == "delete": 
    delete_details(args, db)

if args.command == "create_vault": 
    create_vault(db)

if args.command == "load_vault": 
    load_vault(db)


if args.command == "get_vault": 
    get_details(db)

if args.command == "get_site": 
    get_vault_details(args, db)



