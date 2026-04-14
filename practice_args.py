import argparse 


parser = argparse.ArgumentParser(description = 'This is a sample trial')
# parser.add_argument('filename')
# parser.add_argument('count')

# args = parser.parse_args()

# print(f"FileName: {args.filename} \nCount: {args.count}")
# parser.print_help()



subparsers = parser.add_subparsers(dest="command")

add_parser = subparsers.add_parser("add")
add_parser.add_argument("site")

get_parser = subparsers.add_parser("get")
get_parser.add_argument("site")

delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("site")



args = parser.parse_args()

if args.command == "add": 
    print(f"Adding..{args.site}")

elif args.command == "get": 
    print(f"Getting..{args.site}")

elif args.command == "delete": 
    print(f"Deleting..{args.site}")



